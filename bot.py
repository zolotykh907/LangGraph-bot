from typing import TypedDict
from datetime import datetime, timezone
from langgraph.graph import StateGraph
from langchain_ollama import OllamaLLM


State = TypedDict("State", {"user_input": str, "output": str})

def get_current_time() -> dict:
    """Return the current UTC time in ISO‑8601 format.
    Example → {"utc": "2025‑05‑21T06:42:00Z"}"""

    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {"utc": current_time}

def is_time(input_text: str, llm: OllamaLLM) -> bool:
    """Проверим, содержит ли текст слова, связанные со временем, быстрая проверка"""
    time_words = ["time now", "current time", "который час", "сколько времени"]
    lower_input = input_text.lower()

    for time_word in time_words:  
        if time_word in lower_input:
            return True
    
    prompt = f"""Определи, просит ли пользователь назвать текущее время. 
    Ответ должен содержать строго одно слово: "YES" или "NO".
    Запрос: "{input_text}"
    """
    
    """Получаем ответ от модели, так как вопрос 
    не обязательно может содержать слова, связанные со временем.
    Требует больше времени, так как вызывается LLM, но это дает большую гибкость"""
    answer = llm.invoke(prompt).strip()
    up_answer = answer.upper()  

    if up_answer not in ["YES", "NO"]:              
        raise ValueError("LLM answer not YES or NO")
    
    if up_answer == "NO":
        return False
    
    return True

def message_process(state: State) -> State:
    llm = OllamaLLM(model="llama3")
    user_input = state["user_input"]

    if is_time(user_input, llm):
        current_time = get_current_time()["utc"]
        return {"user_input": user_input, "output": current_time}
    
    return {"user_input": user_input, "output": llm.invoke(user_input)}


app = (
    StateGraph(State)
    .add_node("process", message_process)
    .add_edge("__start__", "process")
    .compile()
)


if __name__ == "__main__":
    print("Добро пожаловать в чат-бот!\n" \
        "Введите 'exit' или 'выход' для выхода.\n")
    while True:
        user_input = input("Вы: ")
        
        if user_input.lower() in ["exit", "выход"]:
            break

        res = app.invoke({"user_input": user_input, "output": ""})
        print("Ответ:", res["output"])