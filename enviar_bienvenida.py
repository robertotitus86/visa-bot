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
# Caso activo: Freddy Wilfrido Vasconez Freire.
CASO = {
    "tratamiento": "Estimado Freddy",
    "email": "freddyvasc@hotmail.com",
    "bcc": ["nanotiendaec@gmail.com"],
    "simulador": "https://www.asesoriadevisadosglobal.com/freddy-vasconez.html",
    "pdf": "pdf-freddy-vasconez.pdf",
    "pdf_extra": ["pdf-freddy-vasconez-checklist.pdf", "pdf-freddy-vasconez-guia-uso.pdf"],
    "fortalezas": [
        "Vives y trabajas en el mismo lugar, en Ibarra — arraigo verificable",
        "Ingreso declarado de $3,000 mensuales y viaje autofinanciado",
        "Sin rechazos previos, sin familiares ni contactos en EE.UU. y pasaporte nuevo vigente hasta 2035",
        "Viaje corto (6 dias) con reserva de hotel concreta en Miami Springs",
    ],
    "cita_texto": "Lunes 9 de noviembre 2026, 9:00 AM",
    "lugar": "Embajada de EE.UU. en Quito &middot; Avigiras E12-170 y Guayacanes, frente al Hospital SOLCA",
    "asunto": "Bienvenida — Tu simulador de entrevista esta listo — Asesoria Visa Global",
}

# Shirma Cortes y Michelle Revelo: cita 13 agosto 2026 ya paso — casos cerrados (19 ago 2026).
# Paola Samaniego y Karen Beltran: casos cerrados (31 ago 2026).


def _html_bienvenida(caso: dict) -> str:
    fortalezas_html = "".join(f"&#8226; {f}<br>" for f in caso["fortalezas"])
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#F1F5F9;font-family:'Segoe UI',Arial,sans-serif;">
<div style="max-width:580px;margin:0 auto;padding:20px;">

  <div style="background:linear-gradient(135deg,#060E1C,#0F1F38);border-radius:16px 16px 0 0;
              padding:28px;border-bottom:3px solid #F5C842;">
    <p style="color:#F5C842;font-size:10px;font-weight:700;letter-spacing:2px;
              text-transform:uppercase;margin:0 0 8px;">Asesoría Visa Global &middot; Preparación Entrevista USA</p>
    <h1 style="color:#fff;font-size:20px;margin:0;line-height:1.4;">
      {caso['tratamiento']},<br>
      <span style="color:#F5C842;">tu simulador de entrevista está listo</span>
    </h1>
  </div>

  <div style="background:#fff;padding:28px;border-radius:0 0 16px 16px;
              box-shadow:0 4px 20px rgba(0,0,0,.08);">

    <p style="color:#475569;font-size:15px;line-height:1.7;margin:0 0 14px;">
      Tu asesoría está en marcha y quiero que tengas todo lo que necesitas para llegar a esa entrevista con una seguridad que la mayoría de aplicantes nunca tiene.
    </p>

    <p style="color:#475569;font-size:15px;line-height:1.7;margin:0 0 14px;">
      Esto no es un proceso genérico. Todo lo que preparamos contigo está basado en tus datos reales del DS-160 y en tu perfil específico. No hay plantillas. No hay copiar y pegar.
    </p>

    <p style="color:#475569;font-size:15px;line-height:1.7;margin:0 0 14px;">
      Con 86 visas aprobadas y un método que hemos afinado durante años, sabemos exactamente qué busca el oficial consular y cómo presentar tu perfil para que hable solo.
    </p>

    <div style="background:#F0FDF4;border-left:4px solid #10B981;
                border-radius:0 10px 10px 0;padding:14px 16px;margin:20px 0;">
      <p style="color:#065F46;font-size:11px;font-weight:700;margin:0 0 8px;
                text-transform:uppercase;letter-spacing:1px;">Tu perfil es sólido</p>
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
      Practícalo todos los días. Empieza por el recorrido completo, luego repite solo las preguntas difíciles. En 10-15 minutos diarios estarás más {caso['preparado']} que el 95% de las personas que van a esa entrevista.
    </p>

    <p style="color:#475569;font-size:14px;line-height:1.7;margin:14px 0 0;">
      En los próximos días te enviaré recordatorios con los puntos más importantes. Si tienes alguna duda antes, escríbeme directamente:<br>
      &#128241; WhatsApp: +593 98 784 6751
    </p>

    <p style="color:#1E293B;font-size:14px;margin:20px 0 0;font-weight:600;">
      Vamos con todo.
    </p>

  </div>

  <p style="color:#94A3B8;font-size:10px;text-align:center;margin:14px 0;">
    Roberto Acosta &middot; Asesoría Visa Global &middot; +593 99 444 2512<br>
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
    # Uso: RESEND_API_KEY=xxx python enviar_bienvenida.py
    enviar_bienvenida()
