from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import pdfplumber
import io
from fastapi.responses import PlainTextResponse
import anthropic
import json
import os
import asyncio
import httpx
from system_prompt import SYSTEM_PROMPT
from crm_lookup import buscar_caso_por_telefono, construir_contexto_crm
from analisis_cliente import analizar_sesion_completa
from sheets_integration import guardar_en_sheets
from paypal_integration import crear_orden, verificar_webhook_signature
from onboarding_flow import (
    activar_onboarding_post_pago, activar_followup_lead, activar_followup_caliente,
    cancelar_followups_lead, notificacion_venta_admin,
    mensaje_confirmacion_expediente,
)
from followup_manager import marcar_formulario_completado
from ds160_flow import (
    esta_en_sesion_ds160, procesar_mensaje_ds160, obtener_reporte,
    cancelar_sesion, iniciar_sesion_ds160, obtener_datos_sesion,
)
from schengen_flow import (
    esta_en_sesion_schengen, procesar_mensaje_schengen, obtener_reporte_schengen,
    cancelar_sesion_schengen, iniciar_sesion_schengen, obtener_datos_sesion_schengen,
)
from uk_flow import (
    esta_en_sesion_uk, procesar_mensaje_uk, obtener_reporte_uk,
    cancelar_sesion_uk, iniciar_sesion_uk, obtener_datos_sesion_uk,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.asesoriadevisadosglobal.com", "https://robertotitus86.github.io", "http://localhost", "http://127.0.0.1"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

ANTHROPIC_KEY       = os.getenv("ANTHROPIC_API_KEY")
VERIFY_TOKEN        = os.getenv("VERIFY_TOKEN", "visaglobal2026")
WA_TOKEN            = os.getenv("WA_TOKEN", "")
RENDER_URL          = os.getenv("RENDER_URL", "https://visa-global-bot.onrender.com")
ADMIN_PHONE         = os.getenv("PHONE_NUMBER", "593994442512")
TG_TOKEN            = os.getenv("TELEGRAM_TOKEN", "")
TG_API              = f"https://api.telegram.org/bot{TG_TOKEN}"
SITE_URL            = "https://www.asesoriadevisadosglobal.com"
GAS_URL             = "https://script.google.com/macros/s/AKfycbxAxCDZ5laDTvU-dfxvdAmyE0JmWfGrDbMDNIf3S_OVK1o-rEM9Gbvz0qkTsXj-vC4k/exec"
GEMINI_KEY          = os.getenv("GEMINI_API_KEY", "AIzaSyCphVM6rvGL68pKcdC39v_ikwKOB2VLgx8")
GEMINI_URL          = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
META_API_VERSION    = "v19.0"

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

# Estado en memoria
_tg_debug        = {"last_update": None, "last_send_result": None}  # diagnóstico
conversations    = {}   # phone → historial de mensajes
pending_payments = {}   # order_id → {phone, phone_number_id, nombre, tipo_visa, paquete, precio}
lead_tracking    = {}   # phone → {nombre, phone_number_id, followup_activado}
clientes_activos = set()  # phones que ya pagaron
_msg_buffer: dict = {}   # phone → {"texts": list[str], "phone_number_id": str}
_msg_timers: dict = {}   # phone → asyncio.Task (debounce 3s)

SENALES_CALIENTE = [
    "precio", "cuánto", "cuanto", "costo", "vale", "cobran",
    "paquete", "esencial", "profesional", "vip",
    "quiero", "me interesa", "interesado", "interesada",
    "cómo empiezo", "como empiezo", "cuándo empezamos", "cuando empezamos",
    "reservar", "contratar", "pagar", "me anoto",
    "urgente", "necesito pronto", "viaje es en",
]

DS160_TRIGGERS = [
    "ds160", "ds-160", "ds 160", "formulario usa",
    "datos para visa usa", "formulario visa americana",
    "quiero llenar el ds", "datos para estados unidos",
]
SCHENGEN_TRIGGERS = [
    "schengen", "visa europa", "visa española", "visa spain",
    "visa españa", "formulario europa", "datos para europa",
    "datos schengen", "formulario schengen", "visa france",
    "visa francia", "visa italia", "visa alemania", "visa holanda",
    "datos para la visa", "llenar formulario", "recopilar datos",
    "formulario de visa", "empezar formulario", "quiero llenar",
    "ayuda con el formulario",
]
UK_TRIGGERS = [
    "reino unido", "uk", "united kingdom", "visa uk",
    "visa inglaterra", "visa london", "visa londres",
    "visa british", "formulario uk", "datos reino unido",
    "datos para reino unido", "standard visitor",
]


# ── IA RESPONSE ────────────────────────────────────────────────────────────────

# Cache de contexto CRM para no consultar Sheets en cada mensaje
_crm_cache: dict = {}  # phone -> {"contexto": str, "ref": str}

TRACKING_TRIGGERS = ["mi caso", "mi numero", "seguimiento", "estado de mi visa",
                     "como va mi caso", "como va mi visa", "vg-", "crm-", "ink-"]

async def get_ai_response(phone: str, user_message: str) -> tuple[str, dict | None]:
    """
    Devuelve (texto_respuesta, cierre_info | None).
    Busca el caso del cliente en el CRM antes de responder.
    """
    if phone not in conversations:
        conversations[phone] = []

    # ── Lookup CRM ──────────────────────────────────────────────
    contexto_crm = ""
    msg_lower = user_message.lower()

    # Buscar por telefono si no tenemos cache o si pregunta por su caso
    es_consulta_seguimiento = any(t in msg_lower for t in TRACKING_TRIGGERS)
    tiene_cache = phone in _crm_cache

    if not tiene_cache or es_consulta_seguimiento:
        resultado = await buscar_caso_por_telefono(phone)
        if resultado:
            contexto_crm = construir_contexto_crm(resultado)
            _crm_cache[phone] = {
                "contexto": contexto_crm,
                "ref": resultado["caso"].get("Ref ID", "")
            }
    elif tiene_cache and _crm_cache[phone]["contexto"]:
        contexto_crm = _crm_cache[phone]["contexto"]

    # ── System prompt dinamico ───────────────────────────────────
    system = SYSTEM_PROMPT
    if contexto_crm:
        system = contexto_crm + "\n\n" + SYSTEM_PROMPT

    # ── Llamada a Claude ─────────────────────────────────────────
    conversations[phone].append({"role": "user", "content": user_message})
    history = conversations[phone][-30:]

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=700,
        system=system,
        messages=history,
    )

    bot_reply = response.content[0].text
    conversations[phone].append({"role": "assistant", "content": bot_reply})

    # Detectar cierre de venta
    cierre_info = None
    if "[CERRAR:" in bot_reply:
        try:
            tag_start = bot_reply.index("[CERRAR:") + 8
            tag_end   = bot_reply.index("]", tag_start)
            parts     = bot_reply[tag_start:tag_end].split(":")
            paquete   = parts[0].strip()
            tipo_visa = parts[1].strip() if len(parts) > 1 else "Visa"
            nombre    = parts[2].strip() if len(parts) > 2 else "Cliente"
            cierre_info = {"paquete": paquete, "tipo_visa": tipo_visa, "nombre": nombre}
            bot_reply = bot_reply.replace(f"[CERRAR:{bot_reply[tag_start:tag_end]}]", "").strip()
        except Exception:
            pass

    # Detectar solicitud de pago de diagnóstico
    if "[DIAGNOSTICO]" in bot_reply:
        if not cierre_info:
            cierre_info = {"paquete": "DIAGNOSTICO"}
        bot_reply = bot_reply.replace("[DIAGNOSTICO]", "").strip()

    return bot_reply, cierre_info


async def get_gemini_response(session_id: str, user_message: str) -> str:
    """Respuesta de IA usando Gemini (gratis). Usado por el bot de Telegram."""
    if session_id not in conversations:
        conversations[session_id] = []

    conversations[session_id].append({"role": "user", "content": user_message})
    history = conversations[session_id][-20:]

    # Convertir historial al formato de Gemini
    contents = []
    for msg in history:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": contents,
        "generationConfig": {"maxOutputTokens": 700, "temperature": 0.75},
    }

    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(GEMINI_URL, json=payload)
        r.raise_for_status()
        reply = r.json()["candidates"][0]["content"]["parts"][0]["text"]

    conversations[session_id].append({"role": "assistant", "content": reply})
    return reply


# ── WHATSAPP ───────────────────────────────────────────────────────────────────

def mark_whatsapp_read(message_id: str, phone_number_id: str):
    if not WA_TOKEN or not phone_number_id or not message_id:
        return
    import requests as req
    url = f"https://graph.facebook.com/{META_API_VERSION}/{phone_number_id}/messages"
    headers = {"Authorization": f"Bearer {WA_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "status": "read", "message_id": message_id}
    try:
        req.post(url, headers=headers, json=payload, timeout=5)
    except Exception:
        pass


def send_whatsapp_message(to: str, message: str, phone_number_id: str = ""):
    if not WA_TOKEN or not phone_number_id:
        print(f"[WA] Sin WA_TOKEN o phone_number_id — mensaje no enviado a {to}")
        return
    import requests as req
    url = f"https://graph.facebook.com/{META_API_VERSION}/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {WA_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message[:4096]},
    }
    try:
        r = req.post(url, headers=headers, json=payload, timeout=10)
        if r.status_code != 200:
            print(f"[WA] Error {r.status_code}: {r.text[:200]}")
    except Exception as e:
        print(f"[WA] Excepción enviando mensaje: {e}")


# ── COMPLETAR FORMULARIO (post-pago) ──────────────────────────────────────────

async def completar_formulario(from_number: str, phone_number_id: str,
                               personas: list, datos: list, tipo_visa: str,
                               bloques_reporte: list):
    """Se activa cuando el cliente completa el formulario de datos."""
    # Cancelar recordatorios de formulario (ya lo completó)
    marcar_formulario_completado(from_number)

    # 1. Reporte al admin
    for bloque in bloques_reporte:
        send_whatsapp_message(ADMIN_PHONE, bloque, phone_number_id)

    # 2. Análisis IA
    try:
        analisis_list = analizar_sesion_completa(personas, datos, tipo_visa)
        for analisis in analisis_list:
            send_whatsapp_message(ADMIN_PHONE, analisis, phone_number_id)
    except Exception as e:
        print(f"Error análisis IA: {e}")
        analisis_list = []

    # 3. Guardar en Google Sheets
    try:
        guardar_en_sheets(personas, datos, tipo_visa, from_number, analisis_list)
    except Exception as e:
        print(f"Error Sheets: {e}")

    # 4. Confirmar al cliente
    nombre = personas[0] if personas else "Cliente"
    send_whatsapp_message(from_number, mensaje_confirmacion_expediente(nombre), phone_number_id)


# ── GENERAR LINK PAYPHONE ─────────────────────────────────────────────────────

async def generar_link_payphone(ref: str, amount: int = 50, paquete: str = "DIAGNOSTICO", nombre: str = "Cliente") -> str | None:
    """Llama GAS servidor a servidor, obtiene URL PayPhone, la envuelve en pagar.html."""
    import urllib.parse
    try:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as c:
            r = await c.get(
                f"{GAS_URL}?action=payphone_prepare"
                f"&ref={urllib.parse.quote(ref)}&amount={amount}"
                f"&paquete={paquete}&nombre={urllib.parse.quote(nombre)}"
            )
            data = r.json()
            payphone_url = data.get("url")
            if payphone_url:
                return f"{SITE_URL}/pagar.html?url={urllib.parse.quote(payphone_url, safe='')}"
    except Exception as e:
        print(f"[PayPhone] Error: {e}")
    return None


PRECIOS_PAQUETES = {
    "ESENCIAL": 197, "PROFESIONAL": 265, "VIP": 320,
    "DIAGNOSTICO": 50, "MEXICO": 79, "RENOVACION": 79, "REVISION": 49,
    "URGENTE_ESENCIAL": 247, "URGENTE_PROFESIONAL": 315, "URGENTE_VIP": 370,
}

# ── CERRAR VENTA CON PAYPHONE ──────────────────────────────────────────────────

async def cerrar_venta(from_number: str, phone_number_id: str,
                       paquete: str, tipo_visa: str, nombre: str):
    """Genera link de pago PayPhone y lo envía al cliente."""
    paquete_upper = paquete.upper()
    precio = PRECIOS_PAQUETES.get(paquete_upper, 250)
    ref = f"{paquete_upper}-{from_number[-6:]}-{int(asyncio.get_event_loop().time())}"

    try:
        url_pago = await generar_link_payphone(ref, precio, paquete_upper, nombre)

        if url_pago:
            pending_payments[ref] = {
                "phone": from_number,
                "phone_number_id": phone_number_id,
                "nombre": nombre,
                "tipo_visa": tipo_visa,
                "paquete": paquete_upper,
                "precio": precio,
            }
            send_whatsapp_message(
                from_number,
                f"Perfecto {nombre.split()[0]} 🎯 Aquí tienes el link para confirmar tu lugar:\n\n"
                f"{url_pago}\n\n"
                f"Paquete {paquete.capitalize()}: ${precio} USD — puedes pagar con tarjeta de crédito o débito.\n\n"
                f"En cuanto se confirme el pago arrancamos con tu caso.",
                phone_number_id,
            )
        else:
            raise Exception(data.get("error", "Sin URL de pago"))

    except Exception as e:
        print(f"[PayPhone] Error cerrar_venta: {e}")
        send_whatsapp_message(
            from_number,
            f"Para confirmar tu lugar en el Paquete {paquete.capitalize()} (${precio} USD), "
            f"puedes transferir a:\n\nBanco Pichincha — Cuenta Ahorros\nTitular: Roberto Acosta\n"
            f"Número: 2200449871\n\nEnvía el comprobante aquí mismo y arrancamos.",
            phone_number_id,
        )


# ── MESSAGE BUFFER (debounce para ser más humano) ──────────────────────────────

async def _flush_buffer(from_number: str):
    """Espera 3s; si no llega otro mensaje, procesa todos los acumulados juntos."""
    try:
        await asyncio.sleep(3)
    except asyncio.CancelledError:
        return
    buf = _msg_buffer.pop(from_number, None)
    _msg_timers.pop(from_number, None)
    if not buf:
        return
    combined = "\n".join(buf["texts"])
    await _process_wa_ia(from_number, buf["phone_number_id"], combined)


async def _process_wa_ia(from_number: str, phone_number_id: str, text: str):
    """Procesa un mensaje (o mensajes combinados) con IA y envía respuesta WA."""
    text_lower = text.lower()

    # Activar follow-up en primer contacto
    if from_number not in clientes_activos and from_number not in lead_tracking:
        lead_tracking[from_number] = {"phone_number_id": phone_number_id, "followup_activado": False}

    reply, cierre_info = await get_ai_response(from_number, text)
    send_whatsapp_message(from_number, reply, phone_number_id)

    lead = lead_tracking.get(from_number, {})
    es_caliente = any(s in text_lower for s in SENALES_CALIENTE) or bool(cierre_info)

    if from_number not in clientes_activos:
        if es_caliente and not lead.get("caliente_activado"):
            activar_followup_caliente(from_number, lead.get("nombre", ""), phone_number_id)
            lead_tracking[from_number].update({"followup_activado": True, "caliente_activado": True})
        elif not lead.get("followup_activado"):
            activar_followup_lead(from_number, lead.get("nombre", ""), phone_number_id)
            lead_tracking[from_number]["followup_activado"] = True

    if cierre_info:
        if cierre_info.get("paquete") == "DIAGNOSTICO":
            pay_url = await generar_link_payphone(from_number)
            if pay_url:
                msg_diag = (
                    "El Diagnóstico evalúa tu perfil con los criterios reales del consulado. "
                    "Resultado en 5 minutos — $50.\n\n"
                    f"Paga aquí directamente:\n{pay_url}\n\n"
                    "Y si decides seguir con nosotros, esos $50 se descuentan del plan que elijas."
                )
            else:
                msg_diag = (
                    "El Diagnóstico evalúa tu perfil con los criterios reales del consulado. "
                    f"Resultado en 5 minutos — $50.\n\n{SITE_URL}/diagnostico.html\n\n"
                    "Y si decides seguir con nosotros, esos $50 se descuentan del plan que elijas."
                )
            send_whatsapp_message(from_number, msg_diag, phone_number_id)
        else:
            await cerrar_venta(
                from_number, phone_number_id,
                cierre_info["paquete"], cierre_info["tipo_visa"], cierre_info["nombre"],
            )


# ── HELPERS ───────────────────────────────────────────────────────────────────

def is_ds160_trigger(text: str) -> bool:
    return any(t in text.lower() for t in DS160_TRIGGERS)

def is_schengen_trigger(text: str) -> bool:
    return any(t in text.lower() for t in SCHENGEN_TRIGGERS)

def is_uk_trigger(text: str) -> bool:
    return any(t in text.lower() for t in UK_TRIGGERS)


# ── KEEP ALIVE ────────────────────────────────────────────────────────────────

async def keep_alive():
    await asyncio.sleep(30)
    while True:
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                await c.get(f"{RENDER_URL}/ping")
        except Exception:
            pass
        await asyncio.sleep(240)  # cada 4 minutos — Render duerme a los 15 min


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(keep_alive())


# ── ENDPOINTS ─────────────────────────────────────────────────────────────────

@app.get("/ping")
async def ping():
    return {"status": "ok"}


@app.get("/webhook")
async def verify_webhook(request: Request):
    mode      = request.query_params.get("hub.mode")
    token     = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)
    raise HTTPException(status_code=403, detail="Token inválido")


@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()

    # Meta WhatsApp Business API — ignorar lo que no sean mensajes
    if data.get("object") != "whatsapp_business_account":
        return {"status": "ok"}

    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                if change.get("field") != "messages":
                    continue

                value           = change.get("value", {})
                phone_number_id = value.get("metadata", {}).get("phone_number_id", "")

                for msg in value.get("messages", []):
                    msg_type    = msg.get("type", "")
                    from_number = msg.get("from", "")
                    message_id  = msg.get("id", "")
                    mark_whatsapp_read(message_id, phone_number_id)

                    if msg_type == "text":
                        text = msg.get("text", {}).get("body", "").strip()
                    elif msg_type == "interactive":
                        interactive = msg.get("interactive", {})
                        itype = interactive.get("type", "")
                        if itype == "button_reply":
                            text = interactive.get("button_reply", {}).get("title", "").strip()
                        elif itype == "list_reply":
                            text = interactive.get("list_reply", {}).get("title", "").strip()
                        else:
                            continue
                    else:
                        continue

                    if not text or not from_number:
                        continue

                    text_lower = text.lower()

                    # Opt-out obligatorio por política de Meta
                    if text_lower == "stop":
                        send_whatsapp_message(
                            from_number,
                            "Has cancelado los mensajes de Asesoría Visa Global. Si deseas reactivar, escribe HOLA.",
                            phone_number_id,
                        )
                        continue

                    # Aviso de privacidad en primer contacto (exigido por Meta)
                    if from_number not in conversations:
                        send_whatsapp_message(
                            from_number,
                            "Este chat es atendido por el asistente virtual de Asesoría Visa Global. "
                            "Tu información se usa únicamente para gestionar tu asesoría. "
                            "Escribe STOP si no deseas recibir más mensajes.",
                            phone_number_id,
                        )

                    # ── Cancelar sesiones activas (inmediato, sin buffer) ──
                    if text_lower in ("cancelar", "cancel", "salir", "exit"):
                        for cancelar_fn, esta_fn, msg_cancelar in [
                            (cancelar_sesion, esta_en_sesion_ds160, "Formulario cancelado. Escribe DS-160 cuando quieras retomarlo."),
                            (cancelar_sesion_schengen, esta_en_sesion_schengen, "Formulario cancelado. Escribe 'Europa' cuando quieras retomarlo."),
                            (cancelar_sesion_uk, esta_en_sesion_uk, "Formulario cancelado. Escribe 'Reino Unido' cuando quieras retomarlo."),
                        ]:
                            if esta_fn(from_number):
                                cancelar_fn(from_number)
                                send_whatsapp_message(from_number, msg_cancelar, phone_number_id)
                                break
                        continue

                    # ── Flujos de formulario activos (inmediato, sin buffer) ──
                    if esta_en_sesion_ds160(from_number):
                        respuestas = procesar_mensaje_ds160(from_number, text)
                        if respuestas is None:
                            bloques = obtener_reporte(from_number) or []
                            personas, datos = obtener_datos_sesion(from_number)
                            await completar_formulario(from_number, phone_number_id, personas, datos, "USA DS-160", bloques)
                        else:
                            for r in respuestas:
                                if r: send_whatsapp_message(from_number, r, phone_number_id)
                        continue

                    if esta_en_sesion_uk(from_number):
                        respuestas = procesar_mensaje_uk(from_number, text)
                        if respuestas is None:
                            bloques = obtener_reporte_uk(from_number) or []
                            personas, datos = obtener_datos_sesion_uk(from_number)
                            await completar_formulario(from_number, phone_number_id, personas, datos, "Reino Unido", bloques)
                        else:
                            for r in respuestas:
                                if r: send_whatsapp_message(from_number, r, phone_number_id)
                        continue

                    if esta_en_sesion_schengen(from_number):
                        respuestas = procesar_mensaje_schengen(from_number, text)
                        if respuestas is None:
                            bloques = obtener_reporte_schengen(from_number) or []
                            personas, datos = obtener_datos_sesion_schengen(from_number)
                            await completar_formulario(from_number, phone_number_id, personas, datos, "Schengen", bloques)
                        else:
                            for r in respuestas:
                                if r: send_whatsapp_message(from_number, r, phone_number_id)
                        continue

                    # ── Triggers de formularios — SOLO si ya pagó ───────────
                    if is_ds160_trigger(text_lower) or is_uk_trigger(text_lower) or is_schengen_trigger(text_lower):
                        if from_number in clientes_activos:
                            if is_ds160_trigger(text_lower):
                                send_whatsapp_message(from_number, iniciar_sesion_ds160(from_number), phone_number_id)
                            elif is_uk_trigger(text_lower):
                                send_whatsapp_message(from_number, iniciar_sesion_uk(from_number), phone_number_id)
                            elif is_schengen_trigger(text_lower):
                                send_whatsapp_message(from_number, iniciar_sesion_schengen(from_number), phone_number_id)
                        else:
                            # No ha pagado — ignorar trigger y dejar que la IA continúe la venta
                            pass
                        continue

                    # ── Conversación IA: buffer 3s para acumular mensajes ────
                    if from_number in _msg_timers and not _msg_timers[from_number].done():
                        _msg_timers[from_number].cancel()
                    if from_number not in _msg_buffer:
                        _msg_buffer[from_number] = {"texts": [], "phone_number_id": phone_number_id}
                    _msg_buffer[from_number]["texts"].append(text)
                    _msg_timers[from_number] = asyncio.create_task(_flush_buffer(from_number))

    except Exception as e:
        print(f"Error webhook: {e}")
    return {"status": "ok"}


@app.post("/paypal-webhook")
async def paypal_webhook(request: Request):
    """Recibe notificaciones de pago confirmado desde PayPal."""
    body    = await request.body()
    headers = dict(request.headers)
    data    = json.loads(body)

    if not verificar_webhook_signature(headers, body):
        raise HTTPException(status_code=400, detail="Firma invalida")

    event_type = data.get("event_type", "")

    if event_type == "PAYMENT.CAPTURE.COMPLETED":
        try:
            resource      = data["resource"]
            order_id      = resource.get("supplementary_data", {}).get("related_ids", {}).get("order_id", "")
            custom_id     = resource.get("custom_id", "")  # teléfono del cliente

            # Buscar la orden por order_id o por custom_id (teléfono)
            pago = None
            for oid, info in list(pending_payments.items()):
                if oid == order_id or info["phone"] == custom_id:
                    pago = info
                    del pending_payments[oid]
                    break

            if pago:
                phone          = pago["phone"]
                phone_id       = pago["phone_number_id"]
                nombre         = pago["nombre"]
                paquete        = pago["paquete"]
                precio         = pago["precio"]
                tipo_visa      = pago["tipo_visa"]

                # Marcar como cliente activo (cancela follow-ups de lead)
                clientes_activos.add(phone)
                cancelar_followups_lead(phone)

                # Notificar a Roberto
                send_whatsapp_message(
                    ADMIN_PHONE,
                    notificacion_venta_admin(nombre, phone, paquete, precio, tipo_visa),
                    phone_id,
                )

                # Activar onboarding automático para el cliente
                mensajes = activar_onboarding_post_pago(
                    phone, nombre, paquete, precio, tipo_visa, phone_id
                )
                for m in mensajes:
                    await asyncio.sleep(1.5)
                    send_whatsapp_message(phone, m, phone_id)

        except Exception as e:
            print(f"Error procesando pago PayPal: {e}")

    return {"status": "ok"}


@app.post("/send-followup")
async def send_followup(request: Request):
    """
    Llamado por Google Apps Script cada 30 minutos.
    Envía follow-ups programados que ya están pendientes.
    """
    data           = await request.json()
    telefono       = data.get("telefono", "")
    mensaje        = data.get("mensaje", "")
    phone_number_id = data.get("phone_number_id", "")

    if not all([telefono, mensaje, phone_number_id]):
        return {"status": "error", "detail": "Faltan campos"}

    # No enviar si ya es cliente activo y el mensaje es de lead follow-up
    tipo = data.get("tipo", "")
    if telefono in clientes_activos and tipo.startswith("lead_followup"):
        return {"status": "skip", "detail": "Ya es cliente activo"}

    send_whatsapp_message(telefono, mensaje, phone_number_id)
    return {"status": "sent"}


@app.get("/")
async def root():
    return {"status": "Asesoria Visa Global Bot v7.0 — Sistema automatizado completo"}


@app.post("/web-chat")
async def web_chat(request: Request):
    """Endpoint para el widget de chat en la web. Sin dependencia de WhatsApp."""
    data       = await request.json()
    session_id = data.get("session_id", "web-anonymous")
    message    = data.get("message", "")
    if not message.strip():
        return {"reply": "No entendi tu mensaje. Puedes escribirlo de nuevo.", "quick_replies": []}

    reply, _ = await get_ai_response("web-" + session_id, message)

    # Sugerir respuestas rapidas segun contexto
    msg_lower = reply.lower()
    quick = []
    if any(w in msg_lower for w in ["precio", "paquete", "cuesta", "cobran"]):
        quick = ["Ver paquetes", "Quiero el diagnostico", "Hablar con Roberto"]
    elif any(w in msg_lower for w in ["rechazo", "negaron", "rechazado"]):
        quick = ["Si, me rechazaron", "No, es primera vez", "Ver Paquete VIP"]
    elif any(w in msg_lower for w in ["diagnostico", "$50", "50 dolares"]):
        quick = ["Obtener diagnostico $50", "Primero tengo preguntas"]
    elif any(w in msg_lower for w in ["hola", "buenos", "buenas", "bienvenido"]):
        quick = ["Visa USA", "Visa España/Schengen", "Tengo rechazo previo"]
    else:
        quick = ["Cuanto cuesta", "Como funciona", "Hablar con Roberto"]

    return {"reply": reply, "quick_replies": quick}


@app.post("/test")
async def test_bot(request: Request):
    data    = await request.json()
    message = data.get("message", "Hola")
    phone   = data.get("phone", "test_user")
    reply, cierre = await get_ai_response(phone, message)
    return {"reply": reply, "cierre_detectado": cierre}


@app.delete("/reset/{phone}")
async def reset_conversation(phone: str):
    for d in [conversations, pending_payments, lead_tracking]:
        d.pop(phone, None)
    clientes_activos.discard(phone)
    cancelar_sesion(phone)
    return {"status": "reiniciado", "phone": phone}


# ── Endpoint: extracción de texto desde PDFs (DS-160 anteriores) ──
@app.post("/extract-pdfs")
async def extract_pdfs(files: List[UploadFile] = File(...)):
    """
    Recibe hasta 5 archivos PDF, extrae el texto de cada uno con pdfplumber
    y lo devuelve como JSON. Usado desde admin.html para analizar DS-160 anteriores.
    """
    if len(files) > 5:
        raise HTTPException(status_code=400, detail="Maximo 5 archivos por solicitud")

    resultados = []
    for f in files:
        contenido = await f.read()
        texto = ""
        try:
            with pdfplumber.open(io.BytesIO(contenido)) as pdf:
                texto = "\n".join(p.extract_text() or "" for p in pdf.pages).strip()
        except Exception as e:
            texto = f"(error al extraer: {str(e)})"

        resultados.append({
            "nombre": f.filename,
            "caracteres": len(texto),
            "texto": texto[:8000]  # max 8000 chars por PDF para no saturar la IA
        })

    return {
        "ok": True,
        "total_archivos": len(resultados),
        "archivos": resultados
    }


# ══════════════════════════════════════════════════════════════════════════════
# TELEGRAM BOT
# ══════════════════════════════════════════════════════════════════════════════

async def tg_typing(chat_id: int):
    """Muestra indicador 'escribiendo...' en Telegram por ~2s."""
    if not TG_TOKEN:
        return
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            await c.post(f"{TG_API}/sendChatAction", json={"chat_id": chat_id, "action": "typing"})
        await asyncio.sleep(1.5)
    except Exception:
        pass


async def tg_send(chat_id: int, text: str, buttons: list = None, parse_mode: str = None):
    """Envía mensaje de Telegram con botones opcionales."""
    if not TG_TOKEN:
        return
    text = text[:4096]
    payload = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    if buttons:
        payload["reply_markup"] = {"inline_keyboard": buttons}
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(f"{TG_API}/sendMessage", json=payload)
            _tg_debug["last_send_result"] = {"status": r.status_code, "body": r.text[:500]}
            if r.status_code != 200:
                print(f"[TG] sendMessage error {r.status_code}: {r.text[:300]}")
    except Exception as e:
        _tg_debug["last_send_result"] = {"error": str(e)}
        print(f"[TG] send exception: {e}")


async def tg_notify_admin(text: str):
    """Notifica al admin (Roberto) en Telegram."""
    if not TG_TOKEN or not os.getenv("TELEGRAM_ADMIN_CHAT_ID"):
        return
    admin_id = int(os.getenv("TELEGRAM_ADMIN_CHAT_ID"))
    await tg_send(admin_id, text)


def tg_quick_buttons(quick_replies: list) -> list:
    """Convierte quick_replies en filas de botones Telegram."""
    rows = []
    for i in range(0, len(quick_replies), 2):
        row = [{"text": qr, "callback_data": qr[:64]} for qr in quick_replies[i:i+2]]
        rows.append(row)
    return rows


@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    """Webhook principal de Telegram."""
    if not TG_TOKEN:
        return {"ok": True}

    data = await request.json()
    _tg_debug["last_update"] = data  # guardar para diagnóstico

    # ── Callback de botón inline ──────────────────────────────────────────
    if "callback_query" in data:
        cb       = data["callback_query"]
        chat_id  = cb["message"]["chat"]["id"]
        cb_text  = cb.get("data", "")
        cb_id    = cb["id"]
        # Acusar recibo del callback
        try:
            async with httpx.AsyncClient(timeout=5) as c:
                await c.post(f"{TG_API}/answerCallbackQuery", json={"callback_query_id": cb_id})
        except Exception:
            pass
        # Tratar el texto del botón como mensaje con IA
        try:
            await tg_typing(chat_id)
            reply, cierre_cb = await get_ai_response(f"tg-{chat_id}", cb_text)
            btns = None
            if cierre_cb and cierre_cb.get("paquete") == "DIAGNOSTICO":
                pay_url = await generar_link_payphone(str(chat_id))
                url_btn = pay_url or f"{SITE_URL}/diagnostico.html"
                btns = [[{"text": "Hacer mi Diagnostico — $50", "url": url_btn}]]
            elif any(w in reply.lower() for w in ["diagnostico", "$50"]):
                btns = [[{"text": "Hacer mi Diagnostico — $50", "url": f"{SITE_URL}/diagnostico.html"}]]
            await tg_send(chat_id, reply, btns)
        except Exception as e:
            print(f"[TG] Error callback IA: {e}")
            await tg_send(chat_id, "Disculpa, escríbeme al WhatsApp +593 99 444 2512.")
        return {"ok": True}

    # ── Mensaje normal ────────────────────────────────────────────────────
    if "message" not in data:
        return {"ok": True}

    msg        = data["message"]
    chat_id    = msg["chat"]["id"]
    text       = msg.get("text", "").strip()
    first_name = msg.get("from", {}).get("first_name", "")

    if not text:
        return {"ok": True}

    # ── Comandos simples — respuesta directa sin menú ────────────────────
    if text == "/start":
        nombre = f", {first_name}" if first_name else ""
        saludo = (
            f"Hola{nombre}. Soy el asesor de Asesoria Visa Global. "
            "Primera consulta completamente gratis.\n\n"
            "Cuentame: a donde quieres viajar y cual es tu situacion?"
        )
        await tg_send(chat_id, saludo)
        return {"ok": True}

    if text in ("/diagnostico", "/diagnostico@VisaGlobalEC_bot"):
        await tg_send(chat_id,
            "El Diagnostico evalua tu perfil con los criterios reales del consulado — "
            "te dice exactamente que tan solido esta tu caso antes de gastar $185 en la cita. "
            "Resultado en 5 minutos, $50. "
            "Y si decides seguir con nosotros, esos $50 se descuentan del plan que elijas.",
            [[{"text": "Hacer mi Diagnostico — $50", "url": f"{SITE_URL}/diagnostico.html"}]])
        return {"ok": True}

    if text in ("/precios", "/paquetes"):
        await tg_send(chat_id,
            "Nuestros paquetes:\n\n"
            "Esencial $197 - revision completa + guia de entrevista\n"
            "Profesional $250 - el mas solicitado, expediente completo + simulacro\n"
            "VIP $320 - para rechazos previos, estrategia completa\n\n"
            "La evaluacion inicial es gratis. Cuentame tu caso.")
        return {"ok": True}

    # ── Cualquier mensaje → IA ────────────────────────────────────────────
    session_id = f"tg-{chat_id}"
    try:
        await tg_typing(chat_id)
        reply, cierre_tg = await get_ai_response(session_id, text)
        btns = None
        if cierre_tg and cierre_tg.get("paquete") == "DIAGNOSTICO":
            pay_url = await generar_link_payphone(str(chat_id))
            url_btn = pay_url or f"{SITE_URL}/diagnostico.html"
            btns = [[{"text": "Hacer mi Diagnostico — $50", "url": url_btn}]]
        elif any(w in reply.lower() for w in ["diagnostico", "$50", "50 dolares"]):
            btns = [[{"text": "Hacer mi Diagnostico — $50", "url": f"{SITE_URL}/diagnostico.html"}]]
        await tg_send(chat_id, reply, btns)
    except Exception as e:
        _tg_debug["last_send_result"] = {"ai_error": str(e)}
        print(f"[TG] Error IA: {e}")
        await tg_send(chat_id,
            "Disculpa, tuve un problema tecnico. "
            "Escribeme al WhatsApp +593 99 444 2512 y te atiendo de inmediato.")

    # Notificar al admin si es lead caliente
    msg_lower = text.lower()
    if any(s in msg_lower for s in ["quiero", "me interesa", "pagar", "contratar", "cuándo empezamos"]):
        await tg_notify_admin(
            f"Lead caliente en Telegram\n"
            f"Nombre: {first_name} | Chat ID: {chat_id}\n"
            f"Mensaje: {text[:200]}"
        )

    return {"ok": True}


@app.get("/telegram-set-webhook")
async def telegram_set_webhook():
    """Llama una sola vez para registrar el webhook con Telegram."""
    if not TG_TOKEN:
        return {"error": "TELEGRAM_TOKEN no configurado en Render"}
    webhook_url = f"{RENDER_URL}/telegram-webhook"
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.post(f"{TG_API}/setWebhook", json={
            "url": webhook_url,
            "allowed_updates": ["message", "callback_query"]
        })
        return r.json()


@app.get("/telegram-info")
async def telegram_info():
    """Verifica el estado del bot de Telegram."""
    if not TG_TOKEN:
        return {"error": "TELEGRAM_TOKEN no configurado"}
    async with httpx.AsyncClient(timeout=10) as c:
        me = await c.get(f"{TG_API}/getMe")
        wh = await c.get(f"{TG_API}/getWebhookInfo")
        return {"bot": me.json(), "webhook": wh.json()}


@app.get("/telegram-debug")
async def telegram_debug_endpoint():
    """Muestra el último update recibido y resultado del último send."""
    return _tg_debug


@app.get("/test-ai")
async def test_ai():
    """Prueba la conexion con Anthropic directamente."""
    try:
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=50,
            messages=[{"role": "user", "content": "di hola"}],
        )
        return {"ok": True, "respuesta": resp.content[0].text}
    except Exception as e:
        return {"ok": False, "error": str(e), "tipo": type(e).__name__}


@app.get("/test-gemini")
async def test_gemini():
    """Prueba la conexion con Gemini directamente."""
    try:
        async with httpx.AsyncClient(timeout=20) as c:
            r = await c.post(GEMINI_URL, json={
                "contents": [{"role": "user", "parts": [{"text": "di hola en espanol"}]}],
                "generationConfig": {"maxOutputTokens": 50},
            })
            if r.status_code != 200:
                return {"ok": False, "status": r.status_code, "error": r.text[:500]}
            data = r.json()
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            return {"ok": True, "respuesta": reply}
    except Exception as e:
        return {"ok": False, "error": str(e), "tipo": type(e).__name__}


@app.get("/telegram-test/{chat_id}")
async def telegram_test(chat_id: int):
    """Envía un mensaje de prueba al chat_id dado para verificar que tg_send funciona."""
    if not TG_TOKEN:
        return {"error": "TELEGRAM_TOKEN no configurado"}
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.post(f"{TG_API}/sendMessage", json={
            "chat_id": chat_id,
            "text": "Test bot Visa Global: si ves esto, el bot funciona correctamente.",
        })
    return {"status": r.status_code, "response": r.json()}


@app.post("/telegram-webhook-echo")
async def telegram_webhook_echo(request: Request):
    """Echo del webhook para ver exactamente que manda Telegram."""
    body = await request.body()
    print(f"[TG-ECHO] {body.decode()[:500]}")
    return {"ok": True, "received": body.decode()[:200]}
