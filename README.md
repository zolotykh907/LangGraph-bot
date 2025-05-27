# LangGraph-bot

## Описание
Чат-бот с использованием LangGraph и Llama3, без сохранения контекста. Пользователь может общаться с ним. В случае запроса времени вызывается инструмент **get_current_time**. Можно явно не указывать запрос "What time is it?", так как запрос может анализироваться моделью, например "Который час".

## Установка и использование
❗**ВАЖНО**❗ Необходима версия Python >= 3.11

Склонируйте репозиторий, создайте окружение и установите зависимости:
```
git clone https://github.com/zolotykh907/LangGraph-bot.git
cd LangGraph-bot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
Далее нужно получить API ключ
⚙️ [LangChain Smith Settings](https://smith.langchain.com/settings)

Создайте файл .env, скопируйте содержимое из .env_example и вставьте ключ:
```
LANGSMITH_API_KEY=lsv2...
```

❗**Установите Ollama**❗

В боте используется локальная модель llama3, поэтому нужно скачать ее:

```
ollama pull llama3
```
В терминале запустите сервер Ollama, и не закрывайте его:
```
ollama serve
```

Для запуска чат-бота введите:
```
langgraph dev
```
Если все прошло без ошибок, у вас откроется окно в браузере с веб-интерфейсом чата (**Safari не поддерживается**).