from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import anthropic
import json
import os
import asyncio
import httpx
from system_prompt import SYSTEM_PROMPT
from ds160_flow import (
    esta_en_sesion_ds160,
    procesar_mensaje_ds160,
    obtener_reporte,
    cancelar_sesion,
    iniciar_sesion_ds160,
)
from schengen_flow import (
    esta_en_sesion_schengen,
    procesar_mensaje_schengen,
    obtener_reporte_schengen,
    cancelar_sesion_schengen,
    iniciar_sesion_schengen,
)

app = FastAPI()

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "visaglobal2026")
WA_TOKEN = os.getenv("WA_TOKEN", "")
RENDER_URL = os.getenv("RENDER_URL", "https://visa-bot-seqw.onrender.com")
ADMIN_PHONE = os.getenv("PHONE_NUMBER", "593994442512")

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

conversations = {}

DS160_TRIGGERS = [
    "ds160", "ds-160", "ds 160", "formulario usa",
    "datos para visa usa", "formulario visa americana",
    "quiero llenar el ds", "datos para estados unidos",
]

SCHENGEN_TRIGGERS = [
    "schengen", "visa europa", "visa española", "visa spain",
    "visa españa", "formulario europa", "datos para europa",
    "visa reino unido", "datos schengen", "formulario schengen",
    "datos para la visa", "llenar formulario", "recopilar datos",
    "formulario de visa", "empezar formulario", "quiero llenar",
    "ayuda con el formulario",
]


def get_ai_response(phone: str, user_message: str) -> str:
    if phone not in conversations:
        conversations[phone] = []

    conversations[phone].append({"role": "user", "content": user_message})
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


def is_ds160_trigger(text: str) -> bool:
    t = text.lower().strip()
    return any(trigger in t for trigger in DS160_TRIGGERS)


def is_schengen_trigger(text: str) -> bool:
    t = text.lower().strip()
    return any(trigger in t for trigger in SCHENGEN_TRIGGERS)


async def keep_alive():
    await asyncio.sleep(60)
    while True:
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                await c.get(f"{RENDER_URL}/ping")
        except Exception:
            pass
        await asyncio.sleep(600)


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
            if msg["type"] != "text":
                continue

            from_number = msg["from"]
            text = msg["text"]["body"].strip()
            text_lower = text.lower()

            # Cancelar cualquier sesión activa
            if text_lower in ("cancelar", "cancel", "salir", "exit"):
                if esta_en_sesion_ds160(from_number):
                    cancelar_sesion(from_number)
                    send_whatsapp_message(from_number, "Formulario cancelado. Escribe DS-160 cuando quieras retomarlo. ¿En qué más te ayudo?", phone_number_id)
                    continue
                if esta_en_sesion_schengen(from_number):
                    cancelar_sesion_schengen(from_number)
                    send_whatsapp_message(from_number, "Formulario cancelado. Escribe 'Schengen' o 'Europa' cuando quieras retomarlo. ¿En qué más te ayudo?", phone_number_id)
                    continue

            # Si está en sesión DS-160 activa
            if esta_en_sesion_ds160(from_number):
                respuestas = procesar_mensaje_ds160(from_number, text)
                if respuestas is None:
                    bloques = obtener_reporte(from_number)
                    if bloques:
                        for bloque in bloques:
                            send_whatsapp_message(ADMIN_PHONE, bloque, phone_number_id)
                    send_whatsapp_message(
                        from_number,
                        "✅ *¡Perfecto! Tengo todos los datos del DS-160.*\n\n"
                        "Roberto ya los recibió y coordinará contigo el llenado del formulario.\n\n"
                        "¿Tienes alguna otra consulta?",
                        phone_number_id
                    )
                else:
                    for r in respuestas:
                        if r:
                            send_whatsapp_message(from_number, r, phone_number_id)
                continue

            # Si está en sesión Schengen activa
            if esta_en_sesion_schengen(from_number):
                respuestas = procesar_mensaje_schengen(from_number, text)
                if respuestas is None:
                    bloques = obtener_reporte_schengen(from_number)
                    if bloques:
                        for bloque in bloques:
                            send_whatsapp_message(ADMIN_PHONE, bloque, phone_number_id)
                    send_whatsapp_message(
                        from_number,
                        "✅ *¡Perfecto! Tengo todos tus datos para la visa Schengen.*\n\n"
                        "Roberto ya los recibió y se pondrá en contacto para continuar con el expediente.\n\n"
                        "¿Tienes alguna otra consulta?",
                        phone_number_id
                    )
                else:
                    for r in respuestas:
                        if r:
                            send_whatsapp_message(from_number, r, phone_number_id)
                continue

            # Activar flujo DS-160 (USA)
            if is_ds160_trigger(text_lower):
                primer_mensaje = iniciar_sesion_ds160(from_number)
                send_whatsapp_message(from_number, primer_mensaje, phone_number_id)
                continue

            # Activar flujo Schengen (Europa/España/UK)
            if is_schengen_trigger(text_lower):
                primer_mensaje = iniciar_sesion_schengen(from_number)
                send_whatsapp_message(from_number, primer_mensaje, phone_number_id)
                continue

            # Flujo normal con Claude
            reply = get_ai_response(from_number, text)
            send_whatsapp_message(from_number, reply, phone_number_id)

    except Exception as e:
        print(f"Error: {e}")
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"status": "Asesoria Visa Global Bot activo", "version": "4.0"}


@app.post("/test")
async def test_bot(request: Request):
    data = await request.json()
    message = data.get("message", "Hola")
    phone = data.get("phone", "test_user")
    reply = get_ai_response(phone, message)
    return {"reply": reply}


@app.post("/test-ds160")
async def test_ds160(request: Request):
    data = await request.json()
    phone = data.get("phone", "test_ds160")
    message = data.get("message", "DS-160")
    if not esta_en_sesion_ds160(phone) and is_ds160_trigger(message.lower()):
        primer = iniciar_sesion_ds160(phone)
        return {"reply": primer, "fase": "inicio"}
    respuestas = procesar_mensaje_ds160(phone, message)
    if respuestas is None:
        bloques = obtener_reporte(phone)
        return {"reply": "COMPLETADO", "reporte": bloques}
    return {"reply": respuestas}


@app.delete("/reset/{phone}")
async def reset_conversation(phone: str):
    if phone in conversations:
        del conversations[phone]
    cancelar_sesion(phone)
    return {"status": "conversacion reiniciada", "phone": phone}
