from typing import TypedDict
import os
from datetime import datetime, timezone
from langchain_ollama import OllamaLLM
from langgraph.graph import StateGraph

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from scripts.tools import *


State = TypedDict("State", {"user_input": str, "output": str})

documents = [
    "Python — это язык программирования.",
    "FAISS используется для векторного поиска.",
    "LangChain помогает строить цепочки для LLM.",
    "Ollama — это локальный запуск LLM.",
    "Имя твоего создателя - Игорь."
]

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(documents)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

def semantic_search(query: str, k: int = 2) -> str:
    query_vec = model.encode([query])
    distances, indices = index.search(np.array(query_vec), k)
    results = [documents[i] for i in indices[0]]
    return "\n".join(results)

def check_tools(input_text: str, llm: OllamaLLM) -> str:
    prompt = f"""
Ты агент, определяющий, какой инструмент использовать:
- Если пользователь просит время, ответь "TIME"
- Если пользователь хочет список файлов, ответь "FILES"
- Если пользователь хочет найти информацию в документах — ответь "SEARCH"
- Если ничего из этого — ответь "NO".

Ответ строго одно слово: TIME, FILES, SEARCH или NO.
Запрос: "{input_text}"
"""
    answer = llm.invoke(prompt).strip().upper()

    if answer not in ["TIME", "FILES", "SEARCH", "NO"]:
        raise ValueError("Ответ модели не соответствует ожидаемому формату")
    
    return answer

def message_process(state: State) -> State:
    llm = OllamaLLM(model="llama3")
    user_input = state["user_input"]
    tool = check_tools(user_input, llm)

    if tool == "TIME":
        answer = get_current_time()["utc"]
    elif tool == "FILES":
        answer = "\n".join(get_all_files()["files"])
    elif tool == "SEARCH":
        context = semantic_search(user_input)
        prompt = f"Контекст:\n{context}\n\nВопрос: {user_input}\nОтвет:"
        answer = llm.invoke(prompt)
    else:
        answer = llm.invoke(user_input)

    return {"user_input": user_input, "output": answer}

app = (
    StateGraph(State)
    .add_node("process", message_process)
    .add_edge("__start__", "process")
    .compile()
)

if __name__ == "__main__":
    print("Добро пожаловать в чат-бот!\nВведите 'exit' или 'выход' для выхода.\n")
    while True:
        user_input = input("Вы: ")
        if user_input.lower() in ["exit", "выход"]:
            break
        res = app.invoke({"user_input": user_input, "output": ""})
        print("Бот:", res["output"])