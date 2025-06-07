from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from bot2 import app as bot_app

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class ChatInput(BaseModel):
    user_input: str

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "bot_reply": None})

@app.post("/chat")
async def chat(query: ChatInput):
    state = {"user_input": query.user_input, "output": ""}
    result = bot_app.invoke(state)
    return {"response": result["output"]}
