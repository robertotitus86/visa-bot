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
    {
        "id": "seas_guaman",
        "cita": date(2026, 7, 1),
        "cita_texto": "Miercoles 1 julio 2026 · 7:30 AM",
        "lugar": "Consulado Quito · Avigiras E12-170, frente al Hospital SOLCA",
        "simulador": "https://www.asesoriadevisadosglobal.com/familia-seas-guaman.html",
        "preguntas": "35 preguntas",
        "zoom_html": (
            "Domingo 15 de junio 2026 · 7:00 PM<br>"
            "Lunes 29 de junio 2026 · 7:00 PM"
        ),
        "fortalezas_html": (
            "Luis es <strong>Alcalde electo</strong> — vinculo institucional inamovible<br>"
            "Zoila tiene <strong>Farmacia propia</strong> — necesita su presencia<br>"
            "Luis viajo a <strong>4 paises</strong> y siempre regreso<br>"
            "Viaje del <strong>20 al 28 de marzo de 2027</strong>, en el receso de fin del primer trimestre — Zoe y Luis Deoniel vuelven a clases justo despues"
        ),
        "tips": [
            "Practique en voz alta frente al espejo. Si suena natural, el oficial lo percibira con confianza.",
            "Respuestas cortas y directas — 2 o 3 oraciones maximas. Si el oficial quiere mas detalle, pregunta.",
            "Repase la respuesta sobre la hermana Alexandra: honesta, tranquila y con enfasis en sus raices en Ecuador.",
            "Luis: recuerde mencionar las sesiones del concejo municipal del 5 de abril como razon de regreso.",
            "Zoila: su farmacia necesita su presencia. Eso es suficiente razon para regresar.",
            "El viaje es del 20 al 28 de marzo de 2027, en el receso de fin del primer trimestre — Zoe y Luis Deoniel regresan a clases justo despues, otro motivo claro de regreso.",
            "Hotel Monreale Express & Studios en Orlando — tengan el numero de confirmacion listo.",
        ],
        "destinatarios": [
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
        ],
    },
    {
        "id": "cesar_castro",
        "cita": date(2026, 7, 14),
        "cita_texto": "Lunes 14 julio 2026 · 7:30 AM",
        "lugar": "Embajada EE.UU. · Avigiras E12-170, frente al Hospital SOLCA",
        "simulador": "https://www.asesoriadevisadosglobal.com/cesar-castro.html",
        "preguntas": "30 preguntas",
        "zoom_html": (
            "Domingo 6 de julio 2026 · 7:00 PM<br>"
            "Sabado 12 de julio 2026 · 7:00 PM"
        ),
        "fortalezas_html": (
            "Cesar es <strong>Alcalde de Santa Clara en ejercicio</strong> — vinculo institucional inamovible<br>"
            "Es <strong>Presidente del COMAGA</strong> — viaje tiene proposito institucional real y verificable<br>"
            "Ingresos documentados y estables: <strong>$4.474/mes</strong><br>"
            "Sin familiares en USA, sin rechazos previos — perfil limpio<br>"
            "Tiene <strong>sesiones de cabildo el 6 de agosto</strong> — garantia de regreso"
        ),
        "tips": [
            "Practique en voz alta frente al espejo. Si suena natural, el oficial lo percibira con confianza.",
            "Respuestas cortas y directas — 2 o 3 oraciones maximas. Si el oficial quiere mas detalle, pregunta.",
            "Proposito del viaje: COMAGA + Comite Civico Ecuatoriano en Elmhurst, Queens, Nueva York.",
            "Garantia de regreso: Alcalde en ejercicio, sesiones de cabildo el 6 de agosto en Santa Clara.",
            "Primera vez en USA: primera oportunidad institucional para representar al COMAGA en Nueva York.",
            "Si preguntan por el contacto en USA: el contacto es institucional — el Comite Civico Ecuatoriano como organizacion.",
            "Llegue a las 7:00 AM (30 minutos antes), sin celular, ropa formal, carpeta con documentos.",
        ],
        "cc_visibles": ["blankytorres27@gmail.com", "janiobunshe@gmail.com"],
        "destinatarios": [
            {
                "nombre": "Cesar", "tratamiento": "Estimado Sr. Alcalde",
                "email": "castroromulo1977@gmail.com", "telefono": "593992564507", "miembro": "cesar",
                "pdf": "pdf-cesar-castro.pdf",
            },
        ],
    },
    {
        "id": "rodriguez_masache",
        "cita": date(2026, 7, 31),
        "cita_texto": "Viernes 31 julio 2026 · 8:30 AM",
        "lugar": "Consulado Quito · Avigiras E12-170, frente al Hospital SOLCA",
        "simulador": "https://www.asesoriadevisadosglobal.com/familia-rodriguez-masache.html",
        "preguntas": "36 preguntas",
        "zoom_html": (
            "Domingo 12 de julio 2026 · 7:00 PM<br>"
            "Domingo 26 de julio 2026 · 7:00 PM"
        ),
        "fortalezas_html": (
            "Paul Fernando es <strong>Alcalde de Paquisha</strong> desde 2023, en campana de reeleccion — vinculo institucional inamovible<br>"
            "Jenny es <strong>Presidenta del Patronato de Accion Social de Paquisha</strong> desde 2023 (desde la eleccion de Paul Fernando como Alcalde)<br>"
            "Jenny administra la <strong>Granja Familiar de Criadero Porcino \"El Piolin\"</strong> desde su mayoria de edad<br>"
            "Paul Fernando fue Policia Nacional 15 anos y viajo a <strong>Espana y Peru</strong>, siempre regreso<br>"
            "Viaje del <strong>21 al 28 de marzo de 2027</strong> — Mileidy y Paul Smith vuelven a clases el 29 de marzo"
        ),
        "tips": [
            "Practique en voz alta frente al espejo. Si suena natural, el oficial lo percibira con confianza.",
            "Respuestas cortas y directas — 2 o 3 oraciones maximas. Si el oficial quiere mas detalle, pregunta.",
            "Si preguntan por la negativa de noviembre 2025: reconozcanla con calma. Paul Fernando fue alcalde desde 2023, Jenny presidenta del Patronato desde 2023.",
            "Paul Fernando: recuerde mencionar su cargo como Alcalde de Paquisha desde 2023, campana de reeleccion, y sus 15 anos en la Policia Nacional.",
            "Jenny: Presidenta del Patronato desde 2023 y administra la granja familiar de criadero porcino El Piolin desde su mayoria de edad — arraigo solido en Paquisha.",
            "El viaje es del 21 al 28 de marzo de 2027 — Mileidy y Paul Smith regresan a clases el 29 de marzo, otro motivo claro de regreso.",
            "Hotel The Point Hotel & Suites en Orlando (7389 Universal Boulevard) — tengan el numero de confirmacion listo.",
        ],
        "destinatarios": [
            {
                "nombre": "Paul Fernando", "tratamiento": "Estimado Sr. Alcalde",
                "email": "paulfernando82@hotmail.com", "telefono": "593985926007", "miembro": "paul",
                "pdf": "pdf-paul-rodriguez.pdf",
            },
            {
                "nombre": "Jenny", "tratamiento": "Estimada Sra. Jenny",
                "email": "masachejenny373@gmail.com", "telefono": "593991468488", "miembro": "jenny",
                "pdf": "pdf-jenny-masache.pdf",
            },
            {
                "nombre": "Mileidy", "tratamiento": "Estimada Mileidy",
                "email": None, "telefono": "593979521411", "miembro": "mileidy",
                "pdf": "pdf-rodriguez-masache.pdf",
            },
        ],
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


def _html_email(familia: dict, tratamiento: str, sim_link: str, cuenta: str) -> str:
    tip = _tip_del_dia(familia)
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
      Su simulador personalizado esta listo con <strong>{familia['preguntas']} basadas en su DS-160 real</strong>.
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
                html     = _html_email(familia, dest["tratamiento"], sim_link, cuenta)
                asunto   = f"{dest['tratamiento']} · Practica de hoy — Entrevista {familia['cita_texto']}"

                payload = {
                    "from": RESEND_FROM,
                    "to": [dest["email"]],
                    "cc": familia.get("cc_visibles", []),
                    "bcc": [GMAIL_USER],
                    "subject": asunto,
                    "html": html,
                }

                pdf_path = os.path.join(PDF_DIR, dest["pdf"])
                if os.path.isfile(pdf_path):
                    with open(pdf_path, "rb") as f:
                        pdf_b64 = base64.b64encode(f.read()).decode("ascii")
                    payload["attachments"] = [{"filename": dest["pdf"], "content": pdf_b64}]
                else:
                    log.warning(f"  [Recordatorios] PDF no encontrado: {pdf_path}")

                r = req.post(
                    "https://api.resend.com/emails",
                    headers={"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"},
                    json=payload,
                    timeout=20,
                )
                if r.status_code in (200, 201, 202):
                    log.info(f"  Email OK -> {dest['nombre']} <{dest['email']}>")
                else:
                    log.error(f"  ERROR -> {dest['nombre']}: {r.status_code} {r.text[:200]}")
            except Exception as e:
                log.error(f"  ERROR -> {dest['nombre']}: {e}")

    log.info("[Recordatorios] Finalizado")
