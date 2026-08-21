"""
Aviso urgente a Paola Samaniego: la entrevista se adelanto del 24 sept al 31 agosto 2026.
Envio unico, fuera del ciclo diario de recordatorios.py.

Uso:
    RESEND_API_KEY=xxx python enviar_cambio_fecha_paola.py
"""
import os
import requests as req

RESEND_FROM = "Asesoria Visa Global <recordatorios@asesoriadevisadosglobal.com>"

CASO = {
    "tratamiento": "Estimada Paola",
    "email": "jsamaniego_1984@hotmail.com",
    "bcc": ["nanotiendaec@gmail.com"],
    "simulador": "https://www.asesoriadevisadosglobal.com/paola-samaniego.html",
    "cita_texto": "Lunes 31 de agosto 2026, 9:30 AM",
    "lugar": "Embajada de EE.UU. en Quito &middot; Avigiras E12-170 y Guayacanes, frente al Hospital SOLCA",
    "sesion1": "Martes 25 de agosto, 10:00 AM (presencial con Roberto)",
    "sesion2": "Jueves 27 de agosto, 10:00 AM (presencial con Roberto)",
    "asunto": "URGENTE — Tu entrevista se adelanto al 31 de agosto — Asesoria Visa Global",
}


def _html(caso: dict) -> str:
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#F1F5F9;font-family:'Segoe UI',Arial,sans-serif;">
<div style="max-width:580px;margin:0 auto;padding:20px;">

  <div style="background:linear-gradient(135deg,#EF4444,#B91C1C);border-radius:16px 16px 0 0;
              padding:28px;border-bottom:3px solid #F5C842;">
    <p style="color:#FEF2F2;font-size:10px;font-weight:700;letter-spacing:2px;
              text-transform:uppercase;margin:0 0 8px;">Asesoria Visa Global &middot; Aviso Urgente</p>
    <h1 style="color:#fff;font-size:20px;margin:0;line-height:1.4;">
      {caso['tratamiento']},<br>
      <span style="color:#F5C842;">tu entrevista se adelanto</span>
    </h1>
  </div>

  <div style="background:#fff;padding:28px;border-radius:0 0 16px 16px;
              box-shadow:0 4px 20px rgba(0,0,0,.08);">

    <p style="color:#475569;font-size:15px;line-height:1.7;margin:0 0 14px;">
      Te escribo con una noticia importante: logramos adelantar tu cita en el consulado. Esto es una buena noticia — significa menos tiempo de espera — pero tambien significa que tenemos que acelerar tu preparacion.
    </p>

    <div style="background:#FEF2F2;border:2px solid #EF4444;border-radius:10px;padding:14px 18px;margin:20px 0;">
      <p style="color:#7F1D1D;font-size:11px;font-weight:700;margin:0 0 8px;text-transform:uppercase;letter-spacing:1px;">Nueva fecha de entrevista</p>
      <p style="color:#1E293B;font-size:14px;margin:0;line-height:1.6;">
        &#128197; <strong>{caso['cita_texto']}</strong><br>
        &#128205; {caso['lugar']}
      </p>
    </div>

    <div style="background:#F0FDF4;border-left:4px solid #10B981;border-radius:0 10px 10px 0;padding:14px 16px;margin:20px 0;">
      <p style="color:#065F46;font-size:11px;font-weight:700;margin:0 0 8px;text-transform:uppercase;letter-spacing:1px;">Sesiones de practica agendadas contigo</p>
      <p style="color:#1E293B;font-size:13px;margin:0;line-height:1.9;">
        &#8226; {caso['sesion1']}<br>
        &#8226; {caso['sesion2']}
      </p>
    </div>

    <p style="color:#475569;font-size:15px;line-height:1.7;margin:0 0 14px;">
      Con menos tiempo, es clave que practiques con el simulador todos los dias hasta la fecha de tu entrevista.
    </p>

    <div style="text-align:center;margin:24px 0;">
      <a href="{caso['simulador']}"
         style="display:inline-block;background:linear-gradient(135deg,#F5C842,#C8861A);
                color:#060E1C;font-weight:800;font-size:15px;padding:16px 40px;
                border-radius:50px;text-decoration:none;">
        Practicar ahora &rarr;
      </a>
    </div>

    <p style="color:#475569;font-size:14px;line-height:1.7;margin:20px 0 0;">
      Nos vemos en las sesiones presenciales. Cualquier duda antes, escribeme directamente:<br>
      &#128241; WhatsApp: +593 98 784 6751
    </p>

    <p style="color:#1E293B;font-size:14px;margin:20px 0 0;font-weight:600;">
      Vamos con todo, tenemos esto listo.
    </p>

  </div>

  <p style="color:#94A3B8;font-size:10px;text-align:center;margin:14px 0;">
    Roberto Acosta &middot; Asesoria Visa Global &middot; +593 99 444 2512<br>
    <a href="https://www.asesoriadevisadosglobal.com" style="color:#94A3B8;">www.asesoriadevisadosglobal.com</a>
  </p>
</div>
</body></html>"""


def enviar(caso: dict = CASO):
    api_key = os.environ.get("RESEND_API_KEY", "")
    if not api_key:
        print("ERROR: falta RESEND_API_KEY en el entorno.")
        return

    payload = {
        "from": RESEND_FROM,
        "to": [caso["email"]],
        "bcc": caso.get("bcc", []),
        "subject": caso["asunto"],
        "html": _html(caso),
    }
    resp = req.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=20,
    )
    print("Status:", resp.status_code)
    print("Respuesta:", resp.text[:500])
    return resp


if __name__ == "__main__":
    enviar()
