import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from config import LLM_CONFIG

client = OpenAI(
    api_key=LLM_CONFIG["api_key"], 
    base_url=LLM_CONFIG["base_url"]
)
app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    system: str = "你是一个乐于助人的助手"


@app.post("/chat")
def chat(req: ChatRequest):
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": req.system},
            {"role": "user", "content": req.message},
        ],
        temperature=0.7,
    )
    return {"reply": response.choices[0].message.content}
