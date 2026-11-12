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
    # Shirma Cortes y Michelle Revelo: cita 13 agosto 2026 ya paso — casos cerrados (19 ago 2026).
    # Paola Samaniego y Karen Beltran: casos cerrados (31 ago 2026).
    # Freddy Vasconez: caso cerrado, visa APROBADA (9 nov 2026).
    {
        "id": "tatiana_witt",
        "cita": date(2026, 11, 16),
        "cita_texto": "Lunes 16 de noviembre 2026, 8:00 AM",
        "lugar": "Embajada EE.UU. Quito · Avigiras E12-170 y Guayacanes, frente al Hospital SOLCA",
        "simulador": "https://www.asesoriadevisadosglobal.com/tatiana-witt.html",
        "preguntas": "más de 20 preguntas (incluye modo oficial consular con preguntas trampa)",
        "fortalezas_html": (
            "&#8226; Trayectoria como Gerente General de CONAFIPS y del Banco de Desarrollo<br>"
            "&#8226; Cargo actual en AME: asesoría técnica a la presidencia<br>"
            "&#8226; Economista con diplomado, MBA y maestría en Cooperación Internacional<br>"
            "&#8226; Viajes previos a 6 países de la región, siempre con retorno a Ecuador<br>"
            "&#8226; Casada, con hogar en Quito y padres en Ecuador; sin rechazos previos"
        ),
        "zoom_html": "Prácticas en vivo con Roberto: <strong>10 y 13 de noviembre</strong>. Te confirmamos la hora por WhatsApp.",
        "tips": [
            "Practica en voz alta frente al espejo. Si suena natural, el oficial lo percibirá con confianza.",
            "Respuestas cortas y directas — 2 o 3 oraciones máximas. Si el oficial quiere más detalle, pregunta.",
            "PUNTO CLAVE: pasaste de Gerente General de CONAFIPS a asesora en AME. Prepara una explicación breve y verdadera de ese cambio.",
            "Ten claros los datos de tu viaje: Miami del 3 al 6 de diciembre y tu contacto Jaime Narváez, del Comité Int Cumbre Lat de New York.",
            "AME paga tu viaje (ten su carta a mano) y el MBA de Andorra y la maestría de Tacna fueron en línea.",
            "Las 2 preguntas obligatorias 2026 sobre daños/persecución: responde con calma, 'No' directo, sin dudar.",
            "Tu cita es el lunes 16 de noviembre a las 8:00 AM. Llega sin celular y con la confirmación del DS-160 impresa.",
        ],
        "destinatarios": [
            {"nombre": "Tatiana", "miembro": "tatiana", "telefono": "593983503495",
             "email": "witttatiana12@gmail.com", "tratamiento": "Estimada Tatiana",
             "pdf": "pdf-tatiana-witt.pdf",
             "pdf_extra": ["pdf-tatiana-witt-checklist.pdf", "pdf-tatiana-witt-guia-uso.pdf"]},
        ],
        "cc_visibles": [],
    },
    {
        "id": "lucia_acosta",
        "cita": date(2026, 11, 18),
        "cita_texto": "Miércoles 18 de noviembre 2026, 8:00 AM",
        "lugar": "Embajada EE.UU. Quito · Avigiras E12-170 y Guayacanes, frente al Hospital SOLCA",
        "simulador": "https://www.asesoriadevisadosglobal.com/lucia-acosta.html",
        "preguntas": "más de 20 preguntas (incluye modo oficial consular con preguntas trampa)",
        "fortalezas_html": (
            "&#8226; 21 años de trayectoria continua en el sector público<br>"
            "&#8226; Cargo de responsabilidad en AME: administración de personal<br>"
            "&#8226; Formación en administración pública (ingeniería, diplomado y maestría)<br>"
            "&#8226; Viaje corto de 3 noches a un evento de negocios en Miami<br>"
            "&#8226; Vive en Portoviejo, con sus padres y familia en Ecuador; sin rechazos previos"
        ),
        "zoom_html": "Roberto agenda las sesiones de practica por WhatsApp segun disponibilidad.",
        "tips": [
            "Practica en voz alta frente al espejo. Si suena natural, el oficial lo percibirá con confianza.",
            "Respuestas cortas y directas — 2 o 3 oraciones máximas. Si el oficial quiere más detalle, pregunta.",
            "PUNTO CLAVE: tus dos hijos son residentes permanentes en EE.UU. Responde con calma y con la verdad: viajas por el evento, tu vida y tu trabajo están en Ecuador, y regresas el 6 de diciembre.",
            "Ten claros los datos de tu viaje: Miami del 3 al 6 de diciembre y tu contacto Jaime Narváez, del Comité Int Cumbre de New York.",
            "Ten claro quién paga tu viaje (el DS-160 no lo indica) y que la maestría de Boston y el diplomado de México fueron virtuales, por eso nunca has viajado a EE.UU.",
            "Las 2 preguntas obligatorias 2026 sobre daños/persecución: responde con calma, 'No' directo, sin dudar.",
            "Tu cita es el miércoles 18 de noviembre a las 8:00 AM. Llega sin celular y con la confirmación del DS-160 impresa.",
        ],
        "destinatarios": [
            {"nombre": "Lucía", "miembro": "lucia", "telefono": "593939406502",
             "email": "luciapiedad.acosta@gmail.com", "tratamiento": "Estimada Lucía",
             "pdf": "pdf-lucia-acosta.pdf",
             "pdf_extra": ["pdf-lucia-acosta-checklist.pdf", "pdf-lucia-acosta-guia-uso.pdf"]},
        ],
        "cc_visibles": [],
    },
    {
        "id": "josue_lopez",
        "cita": date(2026, 11, 23),
        "cita_texto": "Lunes 23 de noviembre 2026, 7:30 AM",
        "lugar": "Embajada EE.UU. Quito · Avigiras E12-170 y Guayacanes, frente al Hospital SOLCA",
        "simulador": "https://www.asesoriadevisadosglobal.com/josue-lopez.html",
        "preguntas": "más de 20 preguntas (incluye modo oficial consular con preguntas trampa)",
        "fortalezas_html": (
            "&#8226; Cargo directivo en AME: cooperación internacional y relaciones con organismos multilaterales<br>"
            "&#8226; Antes, Director de Cooperación Internacional en el Ministerio de Agricultura (2017-2021)<br>"
            "&#8226; Licenciatura en Política y Estudios Internacionales y maestría en Cooperación Internacional<br>"
            "&#8226; Viajes previos a 6 países, siempre con retorno a Ecuador<br>"
            "&#8226; Vive en Quito, con sus padres en Ecuador; sin rechazos previos"
        ),
        "zoom_html": "Prácticas en vivo con Roberto: <strong>18 y 20 de noviembre</strong>. Te confirmamos la hora por WhatsApp.",
        "tips": [
            "Practica en voz alta frente al espejo. Si suena natural, el oficial lo percibirá con confianza.",
            "Respuestas cortas y directas — 2 o 3 oraciones máximas. Si el oficial quiere más detalle, pregunta.",
            "PUNTO CLAVE: estudiaste en Australia y en Corea del Sur. Responde con fechas exactas y deja claro por qué regresaste y qué te ata a Ecuador.",
            "Ten claros los datos de tu viaje: Miami del 3 al 6 de diciembre y tu contacto Jaime Narváez, del Comité Int Cumbre Lat de New York.",
            "AME paga tu viaje (el DS-160 no lo muestra): ten su carta a mano y dilo sin dudar.",
            "Las 2 preguntas obligatorias 2026 sobre daños/persecución: responde con calma, 'No' directo, sin dudar.",
            "Tu cita es el lunes 23 de noviembre a las 7:30 AM. Llega sin celular y con la confirmación del DS-160 impresa.",
        ],
        "destinatarios": [
            {"nombre": "Josué", "miembro": "josue", "telefono": "593960582993",
             "email": "josue90l@gmail.com", "tratamiento": "Estimado Josué",
             "pdf": "pdf-josue-lopez.pdf",
             "pdf_extra": ["pdf-josue-lopez-checklist.pdf", "pdf-josue-lopez-guia-uso.pdf"]},
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
            color = "#F59E0B"; emoji = "Faltan pocos días"
        else:
            color = "#10B981"; emoji = "Sigan practicando"
        return (
            f"<div style='background:#FFF7ED;border:2px solid {color};"
            f"border-radius:10px;padding:14px 18px;margin:16px 0;'>"
            f"<div style='font-size:.8rem;font-weight:700;color:{color};margin-bottom:4px'>"
            f"{emoji} — Faltan {dias} días para la entrevista</div>"
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
    ("{nombre}, un paso más cerca", "Cada practica de hoy suma para llegar con tranquilidad a tu entrevista."),
    ("Hoy toca repasar, {nombre}", "Diez minutos de práctica hoy valen más que una hora la noche anterior."),
    ("{nombre}, sigamos afinando tus respuestas", "Mientras más natural suene, más seguridad vas a sentir."),
    ("Buen día, {nombre} — vamos con todo", "La constancia es lo que marca la diferencia frente al oficial consular."),
    ("{nombre}, repasemos un poco más", "No hace falta perfección, solo naturalidad al responder."),
    ("Un momento para tu preparación, {nombre}", "Aprovecha unos minutos hoy para reforzar tus puntos fuertes."),
    ("{nombre}, tu práctica de hoy te espera", "Cada día que practicas reduces el margen de sorpresas en la cita."),
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


def _html_email(familia: dict, tratamiento: str, sim_link: str, cuenta: str, nombre: str, miembro: str = "") -> str:
    tip = _tip_del_dia(familia)
    from crm_lookup import SHEETS_WEBHOOK
    pixel = (f'<img src="{SHEETS_WEBHOOK}?action=pixelEmail&c={miembro}&d={datetime.now(ZONA):%Y%m%d}" '
             f'width="1" height="1" alt="" style="display:none">')
    titulo_dia, frase_dia = _encabezado_del_dia(nombre)
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#F1F5F9;font-family:'Segoe UI',Arial,sans-serif;">
<div style="max-width:580px;margin:0 auto;padding:20px;">

  <div style="background:linear-gradient(135deg,#060E1C,#0F1F38);border-radius:16px 16px 0 0;
              padding:28px;border-bottom:3px solid #F5C842;">
    <p style="color:#F5C842;font-size:10px;font-weight:700;letter-spacing:2px;
              text-transform:uppercase;margin:0 0 8px;">Asesoría Visa Global · Preparación Entrevista USA</p>
    <h1 style="color:#fff;font-size:20px;margin:0;line-height:1.4;">
      {tratamiento},<br>
      <span style="color:#F5C842;">{titulo_dia}</span>
    </h1>
  </div>

  <div style="background:#fff;padding:28px;border-radius:0 0 16px 16px;
              box-shadow:0 4px 20px rgba(0,0,0,.08);">

    <p style="color:#475569;font-size:15px;line-height:1.7;margin:0 0 14px;">
      {frase_dia} Su simulador personalizado está listo con <strong>{familia['preguntas']} basadas en su DS-160 real</strong>.
    </p>

    {cuenta}

    {familia.get('pago_html', '')}

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
                text-transform:uppercase;letter-spacing:1px;">Consejo del día</p>
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
                text-transform:uppercase;letter-spacing:1px;">Próximas sesiones con Roberto</p>
      <p style="color:#1E293B;font-size:12px;margin:0;line-height:1.8;">
        {familia['zoom_html']}
      </p>
    </div>

  </div>

  {pixel}
  <p style="color:#94A3B8;font-size:10px;text-align:center;margin:14px 0;">
    Asesoría Visa Global · Roberto Acosta · +593 99 444 2512<br>
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


def _abrieron_simulador(horas: int = 24):
    """Devuelve set de nombres (minusculas, sin tildes) que abrieron/practicaron en las ultimas N horas,
    o None si no se pudo consultar (en ese caso NO se manda el empujon, para no acusar en falso)."""
    try:
        from crm_lookup import SHEETS_WEBHOOK
        data = req.get(f"{SHEETS_WEBHOOK}?action=resumenPractica&horas={horas}", timeout=10).json()
        if data.get("status") != "ok":
            return None
        quitar = str.maketrans("áéíóú", "aeiou")
        return {n.lower().translate(quitar) for n, c in data.get("clientes", {}).items()
                if c["aperturas"] or c["respuestas"] or c.get("emails")}
    except Exception as e:
        log.warning(f"[Recordatorios] No pude consultar practica del simulador: {e}")
        return None


def _wa_empujon(familia: dict, nombre: str, miembro: str) -> str:
    """Mensaje cuando NO abrio el simulador en las ultimas 24h."""
    dias = (familia["cita"] - datetime.now(ZONA).date()).days
    sim  = f"{familia['simulador']}?miembro={miembro}"
    return (
        f"Buenos días {nombre} 👋\n\n"
        f"Ayer no vimos que abrieras mi correo ni tu simulador, y faltan *{dias} días* para tu entrevista "
        f"({familia['cita_texto']}).\n\n"
        f"Practicar en voz alta es lo que más ayuda: quien ya ensayó sus respuestas llega más tranquilo "
        f"y responde con seguridad; quien no, suele dudar justo en las preguntas clave.\n\n"
        f"Son solo 15 minutos hoy:\n{sim}\n\n"
        f"Si algo no te cargó o tienes dudas, respóndeme por aquí y lo vemos. Estamos pendientes de tu caso 💪\n\n"
        f"— Roberto · Asesoría Visa Global"
    )


def _html_empujon(dias: int) -> str:
    return (
        "<div style='background:#FEF2F2;border-left:4px solid #EF4444;border-radius:0 10px 10px 0;"
        "padding:14px 16px;margin:16px 0;'><p style='color:#7F1D1D;font-size:13px;margin:0;line-height:1.6;'>"
        f"<strong>Ayer no vimos que abriera nuestro correo ni su simulador</strong> y faltan {dias} días para la entrevista. "
        "Quien ensaya sus respuestas en voz alta llega más tranquilo y responde con seguridad. "
        "Bastan 15 minutos hoy. Si algo no cargó o tiene dudas, respóndanos y lo resolvemos.</p></div>"
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
        abrieron = _abrieron_simulador(24)  # None = no se pudo consultar -> no empujar
        quitar = str.maketrans("áéíóú", "aeiou")
        def _no_abrio(d):
            return abrieron is not None and not any(
                d["miembro"] in v or d["nombre"].lower().translate(quitar) in v for v in abrieron)
        dias_f = (familia["cita"] - hoy_dt).days
        if any(_no_abrio(d) for d in familia["destinatarios"]):
            cuenta += _html_empujon(dias_f)

        # ── WhatsApp (best-effort — requiere ventana 24h activa) ─────────
        for dest in familia["destinatarios"]:
            if _no_abrio(dest):
                wa_msg = _wa_empujon(familia, dest["nombre"], dest["miembro"])
                log.info(f"  [Empujon] {dest['nombre']} no abrio el simulador en 24h")
            else:
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
                html     = _html_email(familia, dest["tratamiento"], sim_link, cuenta, dest["nombre"], dest["miembro"])
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

                nombres_pdf = [dest["pdf"]] + dest.get("pdf_extra", [])
                attachments = []
                for nombre_pdf in nombres_pdf:
                    pdf_path = os.path.join(PDF_DIR, nombre_pdf)
                    if os.path.isfile(pdf_path):
                        with open(pdf_path, "rb") as f:
                            pdf_b64 = base64.b64encode(f.read()).decode("ascii")
                        attachments.append({"filename": nombre_pdf, "content": pdf_b64})
                    else:
                        log.warning(f"  [Recordatorios] PDF no encontrado: {pdf_path}")
                if attachments:
                    payload["attachments"] = attachments

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
