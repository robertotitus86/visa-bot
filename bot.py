from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import anthropic
import json
import os
import asyncio
import httpx
from system_prompt import SYSTEM_PROMPT
from analisis_cliente import analizar_sesion_completa
from sheets_integration import guardar_en_sheets
from paypal_integration import crear_orden, verificar_webhook_signature
from onboarding_flow import (
    activar_onboarding_post_pago, activar_followup_lead,
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

ANTHROPIC_KEY       = os.getenv("ANTHROPIC_API_KEY")
VERIFY_TOKEN        = os.getenv("VERIFY_TOKEN", "visaglobal2026")
WA_TOKEN            = os.getenv("WA_TOKEN", "")
RENDER_URL          = os.getenv("RENDER_URL", "https://visa-global-bot.onrender.com")
ADMIN_PHONE         = os.getenv("PHONE_NUMBER", "593994442512")
GREEN_API_INSTANCE  = os.getenv("GREEN_API_INSTANCE", "7107614197")
GREEN_API_TOKEN     = os.getenv("GREEN_API_TOKEN", "e9bb0092f5e845cea9e281735d92c7ae9663e67a5a654b0c8b")
GREEN_API_BASE      = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE}"

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

# Estado en memoria
conversations    = {}   # phone → historial de mensajes
pending_payments = {}   # order_id → {phone, phone_number_id, nombre, tipo_visa, paquete, precio}
lead_tracking    = {}   # phone → {nombre, phone_number_id, followup_activado}
clientes_activos = set()  # phones que ya pagaron

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

def get_ai_response(phone: str, user_message: str) -> tuple[str, dict | None]:
    """
    Devuelve (texto_respuesta, cierre_info | None).
    cierre_info se llena cuando el bot detecta que debe cerrar la venta.
    El bot incluye [CERRAR:PAQUETE:TIPO_VISA:NOMBRE] en su respuesta para señalizar cierre.
    """
    if phone not in conversations:
        conversations[phone] = []

    conversations[phone].append({"role": "user", "content": user_message})
    history = conversations[phone][-30:]

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=700,
        system=SYSTEM_PROMPT,
        messages=history,
    )

    bot_reply = response.content[0].text
    conversations[phone].append({"role": "assistant", "content": bot_reply})

    # Detectar si el bot quiere cerrar la venta
    cierre_info = None
    if "[CERRAR:" in bot_reply:
        try:
            tag_start = bot_reply.index("[CERRAR:") + 8
            tag_end   = bot_reply.index("]", tag_start)
            parts     = bot_reply[tag_start:tag_end].split(":")
            paquete   = parts[0].strip()   # ESENCIAL / PROFESIONAL / VIP
            tipo_visa = parts[1].strip() if len(parts) > 1 else "Visa"
            nombre    = parts[2].strip() if len(parts) > 2 else "Cliente"
            cierre_info = {"paquete": paquete, "tipo_visa": tipo_visa, "nombre": nombre}
            # Limpiar el tag del texto visible
            bot_reply = bot_reply.replace(f"[CERRAR:{bot_reply[tag_start:tag_end]}]", "").strip()
        except Exception:
            pass

    return bot_reply, cierre_info


# ── WHATSAPP ───────────────────────────────────────────────────────────────────

def send_whatsapp_message(to: str, message: str, phone_number_id: str = ""):
    import requests as req
    chat_id = to if "@" in to else f"{to}@c.us"
    req.post(
        f"{GREEN_API_BASE}/sendMessage/{GREEN_API_TOKEN}",
        json={"chatId": chat_id, "message": message},
        timeout=10,
    )


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


# ── CERRAR VENTA CON PAYPAL ────────────────────────────────────────────────────

async def cerrar_venta(from_number: str, phone_number_id: str,
                       paquete: str, tipo_visa: str, nombre: str):
    """Genera link de pago PayPal y lo envía al cliente."""
    try:
        orden = crear_orden(paquete, from_number)
        order_id = orden["order_id"]
        precio   = orden["precio"]
        url_pago = orden["approval_url"]

        # Guardar orden pendiente
        pending_payments[order_id] = {
            "phone": from_number,
            "phone_number_id": phone_number_id,
            "nombre": nombre,
            "tipo_visa": tipo_visa,
            "paquete": paquete,
            "precio": precio,
        }

        send_whatsapp_message(
            from_number,
            f"Para confirmar tu lugar, realiza el pago aquí:\n\n"
            f"{url_pago}\n\n"
            f"Paquete {paquete.capitalize()}: ${precio} USD\n"
            f"Puedes pagar con tarjeta de crédito o débito a través de PayPal.\n\n"
            f"Una vez confirmado el pago, recibirás acceso inmediato al proceso.",
            phone_number_id,
        )
    except Exception as e:
        print(f"Error creando orden PayPal: {e}")
        send_whatsapp_message(
            from_number,
            "Para confirmar tu reserva, escríbeme y te envío los datos de pago directamente.",
            phone_number_id,
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
    await asyncio.sleep(60)
    while True:
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                await c.get(f"{RENDER_URL}/ping")
        except Exception:
            pass
        await asyncio.sleep(600)


async def configure_green_api():
    await asyncio.sleep(5)
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            await c.post(
                f"{GREEN_API_BASE}/setSettings/{GREEN_API_TOKEN}",
                json={"webhookUrl": f"{RENDER_URL}/webhook", "incomingWebhook": "yes"},
            )
        print("Green API webhook configurado correctamente")
    except Exception as e:
        print(f"Error configurando Green API webhook: {e}")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(keep_alive())
    asyncio.create_task(configure_green_api())


# ── ENDPOINTS ─────────────────────────────────────────────────────────────────

@app.get("/ping")
async def ping():
    return {"status": "ok"}


@app.get("/webhook")
async def verify_webhook():
    return {"status": "ok"}


@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    try:
        # Solo mensajes entrantes de texto (formato Green API)
        if data.get("typeWebhook") != "incomingMessageReceived":
            return {"status": "ok"}

        msg_data    = data.get("messageData", {})
        sender_data = data.get("senderData", {})
        type_msg    = msg_data.get("typeMessage", "")

        if type_msg == "textMessage":
            text = msg_data.get("textMessageData", {}).get("textMessage", "").strip()
        elif type_msg == "extendedTextMessage":
            text = msg_data.get("extendedTextMessageData", {}).get("text", "").strip()
        else:
            return {"status": "ok"}

        if not text:
            return {"status": "ok"}

        chat_id         = sender_data.get("chatId", "")
        from_number     = chat_id.replace("@c.us", "").replace("@g.us", "")
        phone_number_id = GREEN_API_INSTANCE
        text_lower      = text.lower()

        # ── Activar follow-up en primer contacto de lead nuevo ──────
        if from_number not in clientes_activos and from_number not in lead_tracking:
            lead_tracking[from_number] = {
                "phone_number_id": phone_number_id,
                "followup_activado": False,
            }

        # ── Cancelar sesiones activas ───────────────────────────────
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
            return {"status": "ok"}

        # ── Flujos de formulario activos ────────────────────────────
        if esta_en_sesion_ds160(from_number):
            respuestas = procesar_mensaje_ds160(from_number, text)
            if respuestas is None:
                bloques = obtener_reporte(from_number) or []
                personas, datos = obtener_datos_sesion(from_number)
                await completar_formulario(from_number, phone_number_id, personas, datos, "USA DS-160", bloques)
            else:
                for r in respuestas:
                    if r: send_whatsapp_message(from_number, r, phone_number_id)
            return {"status": "ok"}

        if esta_en_sesion_uk(from_number):
            respuestas = procesar_mensaje_uk(from_number, text)
            if respuestas is None:
                bloques = obtener_reporte_uk(from_number) or []
                personas, datos = obtener_datos_sesion_uk(from_number)
                await completar_formulario(from_number, phone_number_id, personas, datos, "Reino Unido", bloques)
            else:
                for r in respuestas:
                    if r: send_whatsapp_message(from_number, r, phone_number_id)
            return {"status": "ok"}

        if esta_en_sesion_schengen(from_number):
            respuestas = procesar_mensaje_schengen(from_number, text)
            if respuestas is None:
                bloques = obtener_reporte_schengen(from_number) or []
                personas, datos = obtener_datos_sesion_schengen(from_number)
                await completar_formulario(from_number, phone_number_id, personas, datos, "Schengen", bloques)
            else:
                for r in respuestas:
                    if r: send_whatsapp_message(from_number, r, phone_number_id)
            return {"status": "ok"}

        # ── Triggers de formularios ─────────────────────────────────
        if is_ds160_trigger(text_lower):
            send_whatsapp_message(from_number, iniciar_sesion_ds160(from_number), phone_number_id)
            return {"status": "ok"}
        if is_uk_trigger(text_lower):
            send_whatsapp_message(from_number, iniciar_sesion_uk(from_number), phone_number_id)
            return {"status": "ok"}
        if is_schengen_trigger(text_lower):
            send_whatsapp_message(from_number, iniciar_sesion_schengen(from_number), phone_number_id)
            return {"status": "ok"}

        # ── Conversación con IA (venta SPIN) ────────────────────────
        reply, cierre_info = get_ai_response(from_number, text)
        send_whatsapp_message(from_number, reply, phone_number_id)

        # Activar follow-up de lead tras primera respuesta del bot
        lead = lead_tracking.get(from_number, {})
        if not lead.get("followup_activado") and from_number not in clientes_activos:
            nombre_lead = lead.get("nombre", "")
            activar_followup_lead(from_number, nombre_lead, phone_number_id)
            lead_tracking[from_number]["followup_activado"] = True

        # Si el bot decidió cerrar la venta → generar link de pago
        if cierre_info:
            await cerrar_venta(
                from_number, phone_number_id,
                cierre_info["paquete"],
                cierre_info["tipo_visa"],
                cierre_info["nombre"],
            )

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


@app.post("/test")
async def test_bot(request: Request):
    data    = await request.json()
    message = data.get("message", "Hola")
    phone   = data.get("phone", "test_user")
    reply, cierre = get_ai_response(phone, message)
    return {"reply": reply, "cierre_detectado": cierre}


@app.delete("/reset/{phone}")
async def reset_conversation(phone: str):
    for d in [conversations, pending_payments, lead_tracking]:
        d.pop(phone, None)
    clientes_activos.discard(phone)
    cancelar_sesion(phone)
    return {"status": "reiniciado", "phone": phone}
