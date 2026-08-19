"""
Recordatorios diarios — Familias en preparacion de entrevista
Se ejecuta cada dia a las 9:00 AM hora Ecuador desde Render.
"""
import base64
import logging
import os
from datetime import datetime, date
import pytz

import requests as req

log = logging.getLogger(__name__)

GMAIL_USER      = os.getenv("GMAIL_USER", "nanotiendaec@gmail.com")
RESEND_API_KEY  = os.getenv("RESEND_API_KEY", "")
RESEND_FROM     = "Asesoria Visa Global <recordatorios@asesoriadevisadosglobal.com>"
WA_TOKEN        = os.getenv("WA_TOKEN", "")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "1132483959957091")
FROM_NAME       = "Asesoria Visa Global"
ZONA            = pytz.timezone("America/Guayaquil")
META_API_VER    = "v19.0"

PDF_DIR = os.path.join(os.path.dirname(__file__), "pdfs")

# ═══════════════════════════════════════════════════════
# FAMILIAS EN PREPARACION
# ═══════════════════════════════════════════════════════
FAMILIAS = [
    # Todos los casos anteriores cerrados (aprobados) - 4 ago 2026

    # PENDIENTE: actualizar "cita" cuando Roberto de la fecha real de la cita
    # consular — hasta entonces no se envian recordatorios diarios (ver check
    # "if familia.get('cita') is None: continue" en enviar_recordatorios()).
    {
        "id": "shirma_cortes",
        "cita": date(2026, 8, 13),
        "cita_texto": "Jueves 13 agosto 2026 · 7:30 AM",
        "lugar": "Consulado Quito · Avigiras E12-170 y Guayacanes, frente al Hospital SOLCA",
        "simulador": "https://www.asesoriadevisadosglobal.com/shirma-cortes.html",
        "preguntas": "15 preguntas (basico/intermedio/dificil)",
        "fortalezas_html": (
            "&#8226; Invitacion oficial de ICLEI a la Semana del Clima de Nueva York<br>"
            "&#8226; Alcaldesa en funciones, cargo publico de maxima autoridad<br>"
            "&#8226; Ingresos verificables y patrimonio/familia en Ecuador<br>"
            "&#8226; Sin rechazos previos, sin familiares en USA"
        ),
        "zoom_html": "Por agendar — se coordinaran sesiones de repaso una vez tengamos fecha de cita.",
        "tips": [
            "Lleva impresa la carta de invitacion oficial de ICLEI a la entrevista — es tu mejor respaldo.",
            "Explica con calma que es un viaje institucional corto, de ocho dias.",
            "Recalca que eres la maxima autoridad electa del municipio y tu regreso es indispensable.",
        ],
        "destinatarios": [
            {"nombre": "Shirma", "miembro": "shirma", "telefono": "593987672577",
             "email": "lacurvadelcanon@hotmail.com", "tratamiento": "Estimada Shirma",
             "pdf": "pdf-shirma-cortes.pdf"},
        ],
        "cc_visibles": [],
    },
    {
        "id": "michelle_revelo",
        "cita": date(2026, 8, 13),
        "cita_texto": "Jueves 13 agosto 2026 · 7:30 AM",
        "lugar": "Consulado Quito · Avigiras E12-170 y Guayacanes, frente al Hospital SOLCA",
        "simulador": "https://www.asesoriadevisadosglobal.com/michelle-revelo.html",
        "preguntas": "15 preguntas (basico/intermedio/dificil)",
        "fortalezas_html": (
            "&#8226; Designada delegada oficial por la Alcaldesa Shirma Cortes<br>"
            "&#8226; Jefa de Uso y Ocupacion de Suelo, perfil tecnico relevante al evento<br>"
            "&#8226; Maestria (IAEN) y empleo publico estable<br>"
            "&#8226; Sin rechazos previos, sin familiares en USA"
        ),
        "zoom_html": "Por agendar — se coordinaran sesiones de repaso una vez tengamos fecha de cita.",
        "tips": [
            "Explica que fuiste designada delegada oficial por la Alcaldesa, no que tienes invitacion propia.",
            "Menciona tu perfil tecnico en uso de suelo como razon de tu designacion.",
            "Si Roberto consigue el oficio de designacion del GAD, llevalo impreso a la entrevista.",
        ],
        "destinatarios": [
            {"nombre": "Michelle", "miembro": "michelle", "telefono": "593987200130",
             "email": "michelle.revelo@iaen.edu.ec", "tratamiento": "Estimada Michelle",
             "pdf": "pdf-michelle-revelo.pdf"},
        ],
        "cc_visibles": [],
    },
    {
        "id": "paola_samaniego",
        "cita": date(2026, 9, 24),
        "cita_texto": "Jueves 24 septiembre 2026 · 7:30 AM (tentativa — gestionando adelantarla)",
        "lugar": "Embajada EE.UU. Quito · Avigiras E12-170 y Guayacanes, frente al Hospital SOLCA",
        "simulador": "https://www.asesoriadevisadosglobal.com/paola-samaniego.html",
        "preguntas": "22 preguntas (incluye modo oficial consular con preguntas trampa)",
        "fortalezas_html": (
            "&#8226; Directora Ejecutiva de la Asociacion de Municipalidades Ecuatorianas (AME) — cargo ejecutivo real y verificable<br>"
            "&#8226; Motivo de viaje institucional documentado: cooperacion AME-ICLEI para la Semana del Clima de Nueva York<br>"
            "&#8226; Casada, esposo y padres en Ecuador — sin familiares en USA, sin rechazos previos<br>"
            "&#8226; Viaje financiado por AME como gasto institucional (vuelos, hospedaje y viaticos)"
        ),
        "zoom_html": "Roberto agenda las sesiones de practica por WhatsApp segun disponibilidad.",
        "tips": [
            "Practique en voz alta frente al espejo. Si suena natural, el oficial lo percibira con confianza.",
            "Respuestas cortas y directas — 2 o 3 oraciones maximas. Si el oficial quiere mas detalle, pregunta.",
            "Si preguntan por su ascenso reciente a Directora Ejecutiva: explique sus 7+ anos de trayectoria en contratacion publica, con seguridad, sin sonar improvisada.",
            "Si preguntan por el contacto en USA marcado como 'no lo conoce': es honesto, el vinculo es institucional con ICLEI, no una persona conocida.",
            "Si preguntan por que viaja sola siendo casada: es un viaje de trabajo por su cargo en AME, no un viaje familiar.",
            "Las 2 preguntas obligatorias 2026 sobre danos/persecucion: responder con calma, 'No' directo, sin dudar.",
            "Llegue 20-30 minutos antes, sin celular, ropa formal, carpeta con documentos originales.",
        ],
        "destinatarios": [
            {"nombre": "Paola", "miembro": "paola", "telefono": "593980881226",
             "email": "jsamaniego_1984@hotmail.com", "tratamiento": "Estimada Paola",
             "pdf": "pdf-paola-samaniego.pdf"},
        ],
        "cc_visibles": [],
    },
]


def _cuenta_regresiva(familia: dict) -> str:
    hoy  = datetime.now(ZONA).date()
    cita = familia["cita"]
    dias = (cita - hoy).days
    if dias > 0:
        if dias <= 7:
            color = "#EF4444"; emoji = "URGENTE"
        elif dias <= 14:
            color = "#F59E0B"; emoji = "Faltan pocos dias"
        else:
            color = "#10B981"; emoji = "Sigan practicando"
        return (
            f"<div style='background:#FFF7ED;border:2px solid {color};"
            f"border-radius:10px;padding:14px 18px;margin:16px 0;'>"
            f"<div style='font-size:.8rem;font-weight:700;color:{color};margin-bottom:4px'>"
            f"{emoji} — Faltan {dias} dias para la entrevista</div>"
            f"<div style='font-size:.9rem;color:#1E293B;'>"
            f"Entrevista: <strong>{familia['cita_texto']}</strong><br>"
            f"{familia['lugar']}</div></div>"
        )
    return ""


def _tip_del_dia(familia: dict) -> str:
    dia = datetime.now(ZONA).timetuple().tm_yday
    tips = familia["tips"]
    return tips[dia % len(tips)]


# Rota el saludo y el enfoque del correo dia a dia para que ningun correo
# se sienta igual al anterior, aunque el tip de abajo coincida. Aplica por
# igual a todos los casos — no mezcla contenido especifico entre clientes.
_ENCABEZADOS = [
    ("{nombre}, un paso mas cerca", "Cada practica de hoy suma para llegar tranquila a tu entrevista."),
    ("Hoy toca repasar, {nombre}", "Diez minutos de practica hoy valen mas que una hora la noche anterior."),
    ("{nombre}, sigamos afinando tus respuestas", "Mientras mas natural suene, mas segura vas a sentirte."),
    ("Buen dia, {nombre} — vamos con todo", "La constancia es lo que marca la diferencia frente al oficial consular."),
    ("{nombre}, repasemos un poco mas", "No hace falta perfeccion, solo naturalidad al responder."),
    ("Un momento para tu preparacion, {nombre}", "Aprovecha unos minutos hoy para reforzar tus puntos fuertes."),
    ("{nombre}, tu practica de hoy te espera", "Cada dia que practicas reduces el margen de sorpresas en la cita."),
]


def _encabezado_del_dia(nombre: str) -> tuple:
    dia = datetime.now(ZONA).timetuple().tm_yday
    titulo, frase = _ENCABEZADOS[dia % len(_ENCABEZADOS)]
    return titulo.format(nombre=nombre), frase


def enviar_email_simple(asunto: str, html: str, to: str = None) -> bool:
    """Envia un correo simple via Resend. Usado como respaldo cuando WhatsApp falla (ventana 24h)."""
    if not RESEND_API_KEY:
        log.error("[Email] RESEND_API_KEY no configurado — email no enviado")
        return False
    try:
        r = req.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"},
            json={
                "from": RESEND_FROM,
                "to": [to or GMAIL_USER],
                "subject": asunto,
                "html": html,
            },
            timeout=20,
        )
        if r.status_code in (200, 201, 202):
            log.info(f"[Email] OK -> {to or GMAIL_USER}")
            return True
        log.error(f"[Email] Error {r.status_code}: {r.text[:200]}")
        return False
    except Exception as e:
        log.error(f"[Email] Excepcion: {e}")
        return False


def _send_wa(telefono: str, mensaje: str):
    """Envía mensaje WhatsApp — best-effort, falla silenciosamente si no hay ventana 24h."""
    if not WA_TOKEN:
        return
    try:
        url = f"https://graph.facebook.com/{META_API_VER}/{PHONE_NUMBER_ID}/messages"
        r = req.post(
            url,
            headers={"Authorization": f"Bearer {WA_TOKEN}", "Content-Type": "application/json"},
            json={"messaging_product": "whatsapp", "to": telefono, "type": "text",
                  "text": {"body": mensaje[:4096]}},
            timeout=10,
        )
        if r.status_code == 200:
            log.info(f"  [WA OK] → {telefono}")
        else:
            log.warning(f"  [WA] Error {r.status_code}: {r.text[:200]}")
    except Exception as e:
        log.warning(f"  [WA] Excepcion: {e}")


def _html_email(familia: dict, tratamiento: str, sim_link: str, cuenta: str, nombre: str) -> str:
    tip = _tip_del_dia(familia)
    titulo_dia, frase_dia = _encabezado_del_dia(nombre)
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#F1F5F9;font-family:'Segoe UI',Arial,sans-serif;">
<div style="max-width:580px;margin:0 auto;padding:20px;">

  <div style="background:linear-gradient(135deg,#060E1C,#0F1F38);border-radius:16px 16px 0 0;
              padding:28px;border-bottom:3px solid #F5C842;">
    <p style="color:#F5C842;font-size:10px;font-weight:700;letter-spacing:2px;
              text-transform:uppercase;margin:0 0 8px;">Asesoria Visa Global · Preparacion Entrevista USA</p>
    <h1 style="color:#fff;font-size:20px;margin:0;line-height:1.4;">
      {tratamiento},<br>
      <span style="color:#F5C842;">{titulo_dia}</span>
    </h1>
  </div>

  <div style="background:#fff;padding:28px;border-radius:0 0 16px 16px;
              box-shadow:0 4px 20px rgba(0,0,0,.08);">

    <p style="color:#475569;font-size:15px;line-height:1.7;margin:0 0 14px;">
      {frase_dia} Su simulador personalizado esta listo con <strong>{familia['preguntas']} basadas en su DS-160 real</strong>.
    </p>

    {cuenta}

    <div style="text-align:center;margin:24px 0;">
      <a href="{sim_link}"
         style="display:inline-block;background:linear-gradient(135deg,#F5C842,#C8861A);
                color:#060E1C;font-weight:800;font-size:15px;padding:16px 40px;
                border-radius:50px;text-decoration:none;">
        Abrir mi simulador personalizado →
      </a>
    </div>

    <div style="background:#F0FDF4;border-left:4px solid #10B981;
                border-radius:0 10px 10px 0;padding:14px 16px;margin:20px 0;">
      <p style="color:#065F46;font-size:11px;font-weight:700;margin:0 0 5px;
                text-transform:uppercase;letter-spacing:1px;">Consejo del dia</p>
      <p style="color:#1E293B;font-size:13px;margin:0;line-height:1.6;">{tip}</p>
    </div>

    <div style="background:#F8FAFC;border-radius:10px;padding:16px;margin:20px 0;">
      <p style="color:#475569;font-size:11px;font-weight:700;margin:0 0 10px;
                text-transform:uppercase;letter-spacing:1px;">Sus fortalezas</p>
      <p style="color:#1E293B;font-size:12px;line-height:2;margin:0;">
        {familia['fortalezas_html']}
      </p>
    </div>

    <div style="background:#EEF2FF;border-radius:10px;padding:14px 16px;margin:20px 0;">
      <p style="color:#3730A3;font-size:11px;font-weight:700;margin:0 0 6px;
                text-transform:uppercase;letter-spacing:1px;">Proximas sesiones con Roberto</p>
      <p style="color:#1E293B;font-size:12px;margin:0;line-height:1.8;">
        {familia['zoom_html']}
      </p>
    </div>

  </div>

  <p style="color:#94A3B8;font-size:10px;text-align:center;margin:14px 0;">
    Asesoria Visa Global · Roberto Acosta · +593 99 444 2512<br>
    <a href="https://www.asesoriadevisadosglobal.com" style="color:#94A3B8;">www.asesoriadevisadosglobal.com</a>
  </p>
</div>
</body></html>"""


def _wa_recordatorio(familia: dict, nombre: str, miembro: str) -> str:
    """Genera el texto corto del recordatorio para WhatsApp."""
    hoy    = datetime.now(ZONA).date()
    cita   = familia["cita"]
    dias   = (cita - hoy).days
    tip    = _tip_del_dia(familia)
    sim    = f"{familia['simulador']}?miembro={miembro}"
    urgencia = f"⏳ Faltan *{dias} días* para la entrevista." if dias > 0 else "🗓 ¡Hoy es la entrevista!"
    return (
        f"Buenos días {nombre} 👋\n\n"
        f"{urgencia}\n"
        f"📅 *{familia['cita_texto']}* — Consulado Quito\n\n"
        f"Tu simulador personalizado está listo:\n{sim}\n\n"
        f"💡 *Consejo de hoy:*\n_{tip}_\n\n"
        f"— Roberto · Asesoría Visa Global"
    )


def enviar_recordatorios():
    """Envia email + WhatsApp diario a todas las familias en preparacion. Llamado por APScheduler."""
    hoy_dt = datetime.now(ZONA).date()
    hoy = datetime.now(ZONA).strftime("%d/%m/%Y %H:%M")
    log.info(f"[Recordatorios] Enviando — {hoy}")

    for familia in FAMILIAS:
        if familia.get("cita") is None:
            log.info(f"[Recordatorios] Saltando {familia['id']} — sin cita agendada todavia")
            continue
        if familia["cita"] < hoy_dt:
            log.info(f"[Recordatorios] Saltando {familia['id']} — cita ya ocurrió ({familia['cita']})")
            continue
        cuenta = _cuenta_regresiva(familia)

        # ── WhatsApp (best-effort — requiere ventana 24h activa) ─────────
        for dest in familia["destinatarios"]:
            wa_msg = _wa_recordatorio(familia, dest["nombre"], dest["miembro"])
            _send_wa(dest["telefono"], wa_msg)

        # ── Email (via Resend HTTP API — Render bloquea SMTP saliente) ────
        if not RESEND_API_KEY:
            log.error("[Recordatorios] RESEND_API_KEY no configurado — email no enviado")
            continue

        for dest in familia["destinatarios"]:
            if not dest.get("email"):
                continue
            try:
                sim_link = f"{familia['simulador']}?miembro={dest['miembro']}"
                html     = _html_email(familia, dest["tratamiento"], sim_link, cuenta, dest["nombre"])
                titulo_dia, _ = _encabezado_del_dia(dest["nombre"])
                asunto   = f"{dest['tratamiento']} · {titulo_dia}"

                payload = {
                    "from": RESEND_FROM,
                    "to": [dest["email"]],
                    "cc": familia.get("cc_visibles", []),
                    "bcc": [GMAIL_USER],
                    "subject": asunto,
                    "html": html,
                }

                pdf_path = os.path.join(PDF_DIR, dest["pdf"])
                attachments = None
                if os.path.isfile(pdf_path):
                    with open(pdf_path, "rb") as f:
                        pdf_b64 = base64.b64encode(f.read()).decode("ascii")
                    attachments = [{"filename": dest["pdf"], "content": pdf_b64}]
                    payload["attachments"] = attachments
                else:
                    log.warning(f"  [Recordatorios] PDF no encontrado: {pdf_path}")

                r = req.post(
                    "https://api.resend.com/emails",
                    headers={"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"},
                    json=payload,
                    timeout=20,
                )
                if r.status_code in (200, 201, 202):
                    log.info(f"  Email OK -> {dest['nombre']} <{dest['email']}> (bcc Roberto)")
                else:
                    log.error(f"  ERROR -> {dest['nombre']}: {r.status_code} {r.text[:200]}")
            except Exception as e:
                log.error(f"  ERROR -> {dest['nombre']}: {e}")

    log.info("[Recordatorios] Finalizado")
