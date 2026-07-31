# chatbot/main.py — Chatbot con OpenAI API + FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os, json

load_dotenv()

app = FastAPI(title="Chatbot API", version="1.0.0")
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    system_prompt: str = "Eres un asistente útil y conciso."
    model: str = "gpt-4o"
    temperature: float = 0.7

# Endpoint de streaming en tiempo real
@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    async def generate():
        stream = await client.chat.completions.create(
            model=req.model,
            temperature=req.temperature,
            stream=True,
            messages=[
                {"role": "system", "content": req.system_prompt},
                *[m.dict() for m in req.messages]
            ]
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            yield f"data: {json.dumps({'delta': delta})}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")

# Endpoint estándar (sin streaming)
@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        resp = await client.chat.completions.create(
            model=req.model,
            temperature=req.temperature,
            messages=[
                {"role": "system", "content": req.system_prompt},
                *[m.dict() for m in req.messages]
            ]
        )
        return {
            "reply": resp.choices[0].message.content,
            "tokens_used": resp.usage.total_tokens,
            "model": resp.model
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health(): return {"status": "ok"}