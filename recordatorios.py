"""
Recordatorios diarios — Familia Seas Guaman
Se ejecuta cada dia a las 9:00 AM hora Ecuador desde Render.
"""
import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime, date
import pytz

import requests as req

log = logging.getLogger(__name__)

GMAIL_USER      = os.getenv("GMAIL_USER", "nanotiendaec@gmail.com")
GMAIL_PASS      = os.getenv("GMAIL_PASS", "")
WA_TOKEN        = os.getenv("WA_TOKEN", "")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "1132483959957091")
FROM_NAME       = "Asesoria Visa Global"
ZONA            = pytz.timezone("America/Guayaquil")
SIMULADOR       = "https://www.asesoriadevisadosglobal.com/familia-seas-guaman.html"
META_API_VER    = "v19.0"

PDF_DIR = os.path.join(os.path.dirname(__file__), "pdfs")

DESTINATARIOS = [
    {
        "nombre": "Luis", "tratamiento": "Estimado Sr. Alcalde",
        "email": "siul_2386@hotmail.com", "telefono": "593997119313", "miembro": "luis",
        "pdf": "pdf-luis-seas.pdf",
    },
    {
        "nombre": "Zoila", "tratamiento": "Estimada Sra. Zoila",
        "email": "zoilyss_@hotmail.es", "telefono": "593988229894", "miembro": "zoila",
        "pdf": "pdf-zoila-guaman.pdf",
    },
]

def _cuenta_regresiva():
    hoy  = datetime.now(ZONA).date()
    cita = date(2026, 7, 1)
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
            f"Entrevista: <strong>Miercoles 1 julio 2026 · 7:30 AM</strong><br>"
            f"Consulado Quito · Avigiras E12-170, frente al Hospital SOLCA</div></div>"
        )
    return ""

TIPS = [
    "Practique en voz alta frente al espejo. Si suena natural, el oficial lo percibira con confianza.",
    "Respuestas cortas y directas — 2 o 3 oraciones maximas. Si el oficial quiere mas detalle, pregunta.",
    "Repase la respuesta sobre la hermana Alexandra: honesta, tranquila y con enfasis en sus raices en Ecuador.",
    "Luis: recuerde mencionar las sesiones del concejo municipal del 5 de abril como razon de regreso.",
    "Zoila: su farmacia necesita su presencia. Eso es suficiente razon para regresar.",
    "Los hijos tienen clases a partir del 28 de julio — ese dato ancla el regreso de toda la familia.",
    "Hotel Monreale Express & Studios en Orlando — tengan el numero de confirmacion listo.",
]

def _tip_del_dia():
    dia = datetime.now(ZONA).timetuple().tm_yday
    return TIPS[dia % len(TIPS)]


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

def _html_email(tratamiento, sim_link, cuenta):
    tip = _tip_del_dia()
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
      <span style="color:#F5C842;">hoy es dia de practicar</span>
    </h1>
  </div>

  <div style="background:#fff;padding:28px;border-radius:0 0 16px 16px;
              box-shadow:0 4px 20px rgba(0,0,0,.08);">

    <p style="color:#475569;font-size:15px;line-height:1.7;margin:0 0 14px;">
      La entrevista consular se acerca y cada dia de practica marca la diferencia.
      Su simulador personalizado esta listo con <strong>35 preguntas basadas en su DS-160 real</strong>.
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
        Luis es <strong>Alcalde electo</strong> — vinculo institucional inamovible<br>
        Zoila tiene <strong>Farmacia propia</strong> — necesita su presencia<br>
        Luis viajo a <strong>4 paises</strong> y siempre regreso<br>
        Los hijos tienen clases a partir del <strong>28 de julio 2026</strong>
      </p>
    </div>

    <div style="background:#EEF2FF;border-radius:10px;padding:14px 16px;margin:20px 0;">
      <p style="color:#3730A3;font-size:11px;font-weight:700;margin:0 0 6px;
                text-transform:uppercase;letter-spacing:1px;">Proximas sesiones con Roberto</p>
      <p style="color:#1E293B;font-size:12px;margin:0;line-height:1.8;">
        Domingo 15 de junio 2026 · 7:00 PM<br>
        Lunes 29 de junio 2026 · 7:00 PM
      </p>
    </div>

  </div>

  <p style="color:#94A3B8;font-size:10px;text-align:center;margin:14px 0;">
    Asesoria Visa Global · Roberto Acosta · +593 99 444 2512<br>
    <a href="https://www.asesoriadevisadosglobal.com" style="color:#94A3B8;">www.asesoriadevisadosglobal.com</a>
  </p>
</div>
</body></html>"""


def _wa_recordatorio(nombre: str, tratamiento: str, miembro: str) -> str:
    """Genera el texto corto del recordatorio para WhatsApp."""
    hoy    = datetime.now(ZONA).date()
    cita   = date(2026, 7, 1)
    dias   = (cita - hoy).days
    tip    = _tip_del_dia()
    sim    = f"{SIMULADOR}?miembro={miembro}"
    urgencia = f"⏳ Faltan *{dias} días* para la entrevista." if dias > 0 else "🗓 ¡Hoy es la entrevista!"
    return (
        f"Buenos días {nombre} 👋\n\n"
        f"{urgencia}\n"
        f"📅 *1 julio 2026 · 7:30 AM* — Consulado Quito\n\n"
        f"Tu simulador personalizado está listo:\n{sim}\n\n"
        f"💡 *Consejo de hoy:*\n_{tip}_\n\n"
        f"— Roberto · Asesoría Visa Global"
    )


def enviar_recordatorios():
    """Envia email + WhatsApp diario a Luis y Zoila. Llamado por APScheduler."""
    hoy    = datetime.now(ZONA).strftime("%d/%m/%Y %H:%M")
    cuenta = _cuenta_regresiva()
    log.info(f"[Recordatorios] Enviando — {hoy}")

    # ── WhatsApp (best-effort — requiere ventana 24h activa) ─────────
    for dest in DESTINATARIOS:
        wa_msg = _wa_recordatorio(dest["nombre"], dest["tratamiento"], dest["miembro"])
        _send_wa(dest["telefono"], wa_msg)

    # ── Email ─────────────────────────────────────────────────────────
    if not GMAIL_PASS:
        log.error("[Recordatorios] GMAIL_PASS no configurado — email no enviado")
        return

    try:
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.starttls()
        smtp.login(GMAIL_USER, GMAIL_PASS)
    except Exception as e:
        log.error(f"[Recordatorios] Error SMTP login: {e}")
        return

    for dest in DESTINATARIOS:
        try:
            sim_link = f"{SIMULADOR}?miembro={dest['miembro']}"
            html     = _html_email(dest["tratamiento"], sim_link, cuenta)
            asunto   = f"{dest['tratamiento']} · Practica de hoy — Entrevista 1 julio 2026"

            msg = MIMEMultipart("mixed")
            msg["Subject"] = asunto
            msg["From"]    = f"{FROM_NAME} <{GMAIL_USER}>"
            msg["To"]      = dest["email"]
            msg["Bcc"]     = GMAIL_USER

            alt = MIMEMultipart("alternative")
            alt.attach(MIMEText(html, "html", "utf-8"))
            msg.attach(alt)

            pdf_path = os.path.join(PDF_DIR, dest["pdf"])
            if os.path.isfile(pdf_path):
                with open(pdf_path, "rb") as f:
                    part = MIMEApplication(f.read(), _subtype="pdf")
                part.add_header("Content-Disposition", "attachment", filename=dest["pdf"])
                msg.attach(part)
            else:
                log.warning(f"  [Recordatorios] PDF no encontrado: {pdf_path}")

            smtp.sendmail(GMAIL_USER, [dest["email"], GMAIL_USER], msg.as_string())
            log.info(f"  Email OK -> {dest['nombre']} <{dest['email']}>")
        except Exception as e:
            log.error(f"  ERROR -> {dest['nombre']}: {e}")

    smtp.quit()
    log.info("[Recordatorios] Finalizado")
