"""
Envia el correo de bienvenida — UNA SOLA VEZ, en el momento de crear un caso nuevo.
No forma parte del ciclo diario de recordatorios.py (ese sigue solo desde el dia 2).

Uso:
    RESEND_API_KEY=xxx python enviar_bienvenida.py

Editar los datos del CASO abajo antes de cada ejecucion.
"""
import os
import base64
import requests as req

RESEND_FROM = "Asesoria Visa Global <recordatorios@asesoriadevisadosglobal.com>"
PDF_DIR = os.path.join(os.path.dirname(__file__), "pdfs")

# ─── EDITAR PARA CADA CLIENTE NUEVO ──────────────────────────────────────────
# Caso activo: Jennifer Paola Samaniego Marines — Directora Ejecutiva AME.
CASO = {
    "tratamiento": "Estimada Paola",
    "email": "jsamaniego_1984@hotmail.com",
    "bcc": ["nanotiendaec@gmail.com"],
    "simulador": "https://www.asesoriadevisadosglobal.com/paola-samaniego.html",
    "pdf": "pdf-paola-samaniego.pdf",
    "pdf_extra": ["pdf-paola-samaniego-checklist.pdf"],
    "fortalezas": [
        "Eres Directora Ejecutiva de la Asociacion de Municipalidades Ecuatorianas (AME), con mas de 7 anos de trayectoria en el sector publico",
        "Viajas por un motivo institucional documentado: cooperacion AME-ICLEI para la Semana del Clima de Nueva York",
        "Casada, con esposo, dos hijos pequenos (6 y 2 anos) y padres en Ecuador — sin familiares en Estados Unidos y sin rechazos previos de visa",
        "El viaje es financiado por AME como gasto institucional (vuelos, hospedaje y viaticos)",
    ],
    "cita_texto": "Jueves 24 de septiembre 2026, 7:30 AM (tentativa — estamos gestionando adelantarla)",
    "lugar": "Embajada de EE.UU. en Quito &middot; Avigiras E12-170 y Guayacanes, frente al Hospital SOLCA",
    "asunto": "Bienvenida — Tu simulador de entrevista esta listo — Asesoria Visa Global",
}

# ─── CASOS NUEVOS — Shirma Cortes & Michelle Revelo (4 ago 2026) ─────────────
# NO enviar hasta que Roberto autorice y tengamos RESEND_API_KEY disponible.
CASO_SHIRMA = {
    "tratamiento": "Estimada Shirma",
    "email": "lacurvadelcanon@hotmail.com",
    "bcc": ["nanotiendaec@gmail.com"],
    "simulador": "https://www.asesoriadevisadosglobal.com/shirma-cortes.html",
    "pdf": "pdf-shirma-cortes.pdf",
    "fortalezas": [
        "Fue invitada oficialmente por ICLEI a la Semana del Clima de Nueva York, evento paralelo a la Asamblea General de la ONU",
        "Alcaldesa en funciones del GAD Municipal de Francisco de Orellana, cargo publico de maxima autoridad",
        "Ingresos verificables ($4,508/mes) y patrimonio y familia en Ecuador",
        "Primer viaje a Estados Unidos, sin rechazos previos, sin familiares en USA",
    ],
    "cita_texto": "POR AGENDAR — DS-160 recien enviado (4 ago 2026)",
    "lugar": "Consulado de Estados Unidos, Quito (por confirmar con la cita)",
    "asunto": "Bienvenida — Tu simulador de entrevista esta listo — Asesoria Visa Global",
}

CASO_MICHELLE = {
    "tratamiento": "Estimada Michelle",
    "email": "michelle.revelo@iaen.edu.ec",
    "bcc": ["nanotiendaec@gmail.com"],
    "simulador": "https://www.asesoriadevisadosglobal.com/michelle-revelo.html",
    "pdf": "pdf-michelle-revelo.pdf",
    "fortalezas": [
        "Designada delegada oficial por la Alcaldesa Shirma Cortes para acompanarla a la Semana del Clima de Nueva York",
        "Jefa de Uso y Ocupacion de Suelo del GAD Fco. de Orellana, perfil tecnico relevante al tema del evento",
        "Maestria en Planificacion y Prospectiva Multisectorial (IAEN) y empleo publico estable",
        "Primer viaje a Estados Unidos, sin rechazos previos, sin familiares en USA",
    ],
    "cita_texto": "POR AGENDAR — DS-160 recien enviado (4 ago 2026)",
    "lugar": "Consulado de Estados Unidos, Quito (por confirmar con la cita)",
    "asunto": "Bienvenida — Tu simulador de entrevista esta listo — Asesoria Visa Global",
}


def _html_bienvenida(caso: dict) -> str:
    fortalezas_html = "".join(f"&#8226; {f}<br>" for f in caso["fortalezas"])
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#F1F5F9;font-family:'Segoe UI',Arial,sans-serif;">
<div style="max-width:580px;margin:0 auto;padding:20px;">

  <div style="background:linear-gradient(135deg,#060E1C,#0F1F38);border-radius:16px 16px 0 0;
              padding:28px;border-bottom:3px solid #F5C842;">
    <p style="color:#F5C842;font-size:10px;font-weight:700;letter-spacing:2px;
              text-transform:uppercase;margin:0 0 8px;">Asesoria Visa Global &middot; Preparacion Entrevista USA</p>
    <h1 style="color:#fff;font-size:20px;margin:0;line-height:1.4;">
      {caso['tratamiento']},<br>
      <span style="color:#F5C842;">tu simulador de entrevista esta listo</span>
    </h1>
  </div>

  <div style="background:#fff;padding:28px;border-radius:0 0 16px 16px;
              box-shadow:0 4px 20px rgba(0,0,0,.08);">

    <p style="color:#475569;font-size:15px;line-height:1.7;margin:0 0 14px;">
      Tu asesoria esta en marcha y quiero que tengas todo lo que necesitas para llegar a esa entrevista con una seguridad que la mayoria de aplicantes nunca tiene.
    </p>

    <p style="color:#475569;font-size:15px;line-height:1.7;margin:0 0 14px;">
      Esto no es un proceso generico. Todo lo que preparamos contigo esta basado en tus datos reales del DS-160 y en tu perfil especifico. No hay plantillas. No hay copiar y pegar.
    </p>

    <p style="color:#475569;font-size:15px;line-height:1.7;margin:0 0 14px;">
      Con 86 visas aprobadas y un metodo que hemos afinado durante anos, sabemos exactamente que busca el oficial consular y como presentar tu perfil para que hable solo.
    </p>

    <div style="background:#F0FDF4;border-left:4px solid #10B981;
                border-radius:0 10px 10px 0;padding:14px 16px;margin:20px 0;">
      <p style="color:#065F46;font-size:11px;font-weight:700;margin:0 0 8px;
                text-transform:uppercase;letter-spacing:1px;">Tu perfil es solido</p>
      <p style="color:#1E293B;font-size:13px;margin:0;line-height:1.9;">
        {fortalezas_html}
      </p>
    </div>

    <p style="color:#475569;font-size:15px;line-height:1.7;margin:0 0 14px;">
      Ahora toca trabajar esas respuestas hasta que salgan de forma natural.
    </p>

    <div style="text-align:center;margin:24px 0;">
      <a href="{caso['simulador']}"
         style="display:inline-block;background:linear-gradient(135deg,#F5C842,#C8861A);
                color:#060E1C;font-weight:800;font-size:15px;padding:16px 40px;
                border-radius:50px;text-decoration:none;">
        Abrir mi simulador personalizado &rarr;
      </a>
    </div>

    <div style="background:#FFF7ED;border:2px solid #F59E0B;border-radius:10px;padding:14px 18px;margin:20px 0;">
      <p style="color:#1E293B;font-size:13px;margin:0;line-height:1.6;">
        &#128197; Tu entrevista: <strong>{caso['cita_texto']}</strong><br>
        &#128205; {caso['lugar']}
      </p>
    </div>

    <p style="color:#475569;font-size:14px;line-height:1.7;margin:20px 0 0;">
      Practicalo todos los dias. Empieza por el recorrido completo, luego repite solo las preguntas dificiles. En 10-15 minutos diarios estaras mas preparada que el 95% de las personas que van a esa entrevista.
    </p>

    <p style="color:#475569;font-size:14px;line-height:1.7;margin:14px 0 0;">
      En los proximos dias te enviare recordatorios con los puntos mas importantes. Si tienes alguna duda antes, escribeme directamente:<br>
      &#128241; WhatsApp: +593 98 784 6751
    </p>

    <p style="color:#1E293B;font-size:14px;margin:20px 0 0;font-weight:600;">
      Vamos con todo.
    </p>

  </div>

  <p style="color:#94A3B8;font-size:10px;text-align:center;margin:14px 0;">
    Roberto Acosta &middot; Asesoria Visa Global &middot; +593 99 444 2512<br>
    <a href="https://www.asesoriadevisadosglobal.com" style="color:#94A3B8;">www.asesoriadevisadosglobal.com</a>
  </p>
</div>
</body></html>"""


def _enviar(payload: dict, api_key: str):
    resp = req.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=20,
    )
    print("Status:", resp.status_code)
    print("Respuesta:", resp.text[:500])
    return resp


def enviar_bienvenida(caso: dict = CASO):
    """Envia la bienvenida al cliente con Roberto en bcc (copia oculta)."""
    api_key = os.environ.get("RESEND_API_KEY", "")
    if not api_key:
        print("ERROR: falta RESEND_API_KEY en el entorno.")
        return

    nombres_pdf = [caso["pdf"]] + caso.get("pdf_extra", [])
    attachments = []
    for nombre_pdf in nombres_pdf:
        pdf_path = os.path.join(PDF_DIR, nombre_pdf)
        if os.path.isfile(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_b64 = base64.b64encode(f.read()).decode("ascii")
            attachments.append({"filename": nombre_pdf, "content": pdf_b64})
        else:
            print(f"AVISO: PDF no encontrado en {pdf_path} — no se adjunta.")

    payload_cliente = {
        "from": RESEND_FROM,
        "to": [caso["email"]],
        "bcc": caso.get("bcc", []),
        "subject": caso["asunto"],
        "html": _html_bienvenida(caso),
    }
    if attachments:
        payload_cliente["attachments"] = attachments

    print("--- Enviando al cliente (con bcc a Roberto) ---")
    _enviar(payload_cliente, api_key)


if __name__ == "__main__":
    import sys
    # Uso: RESEND_API_KEY=xxx python enviar_bienvenida.py [paola|shirma|michelle]
    # Cada caso es independiente — sin argumento se envia CASO (Paola, caso activo).
    CASOS = {"paola": CASO, "shirma": CASO_SHIRMA, "michelle": CASO_MICHELLE}
    if len(sys.argv) > 1 and sys.argv[1] in CASOS:
        enviar_bienvenida(CASOS[sys.argv[1]])
    else:
        enviar_bienvenida()
