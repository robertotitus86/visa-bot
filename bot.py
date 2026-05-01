from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import anthropic
import json
import os
import asyncio
import httpx
from system_prompt import SYSTEM_PROMPT

app = FastAPI()

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "visaglobal2026")
WA_TOKEN = os.getenv("WA_TOKEN", "")
RENDER_URL = os.getenv("RENDER_URL", "https://visa-bot-seqw.onrender.com")

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

# Historial de conversaciones en memoria (por número de teléfono)
conversations = {}


def get_ai_response(phone: str, user_message: str) -> str:
    if phone not in conversations:
        conversations[phone] = []

    conversations[phone].append({"role": "user", "content": user_message})

    # Últimos 30 mensajes para mantener contexto amplio
    history = conversations[phone][-30:]

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=history
    )

    bot_reply = response.content[0].text
    conversations[phone].append({"role": "assistant", "content": bot_reply})
    return bot_reply


def send_whatsapp_message(to: str, message: str, phone_number_id: str):
    import requests
    url = f"https://graph.facebook.com/v21.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {WA_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=payload)


# Keep-alive: se auto-pingea cada 10 minutos para no dormirse en Render free
async def keep_alive():
    await asyncio.sleep(60)  # esperar 1 min antes del primer ping
    while True:
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                await c.get(f"{RENDER_URL}/ping")
        except Exception:
            pass
        await asyncio.sleep(600)  # cada 10 minutos


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(keep_alive())


@app.get("/ping")
async def ping():
    return {"status": "ok"}


@app.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(content=challenge)
    raise HTTPException(status_code=403, detail="Token invalido")


@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        phone_number_id = value["metadata"]["phone_number_id"]
        messages = value.get("messages", [])

        for msg in messages:
            if msg["type"] == "text":
                from_number = msg["from"]
                text = msg["text"]["body"]
                reply = get_ai_response(from_number, text)
                send_whatsapp_message(from_number, reply, phone_number_id)
    except Exception as e:
        print(f"Error: {e}")
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"status": "Asesoria Visa Global Bot activo", "version": "2.0"}


@app.post("/test")
async def test_bot(request: Request):
    data = await request.json()
    message = data.get("message", "Hola")
    phone = data.get("phone", "test_user")
    reply = get_ai_response(phone, message)
    return {"reply": reply}


@app.delete("/reset/{phone}")
async def reset_conversation(phone: str):
    if phone in conversations:
        del conversations[phone]
    return {"status": "conversacion reiniciada", "phone": phone}
