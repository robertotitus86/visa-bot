"""
Recordatorios automáticos por email — César Castro
Entrevista: 14 julio 2026, 7:30 AM
Ejecutar: python enviar_recordatorios_castro.py

Requiere: pip install schedule
Gmail: usar App Password (no contraseña normal)
  → myaccount.google.com → Seguridad → Contraseñas de aplicación
"""
import smtplib, ssl, schedule, time, logging
from datetime import date, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─── CONFIGURAR ───────────────────────────────────────────────────────────────
GMAIL_USER     = "nanotiendaec@gmail.com"
GMAIL_PASSWORD = "mydjjjgvjecvmqmy"
CLIENTE_EMAIL  = "castroromulo1977@gmail.com"
CC_VISIBLES    = ["blankytorres27@gmail.com", "janiobunshe@gmail.com"]
BCC_ROBERTO    = "nanotiendaec@gmail.com"
CLIENTE_NOMBRE = "César"

ENTREVISTA = date(2026, 7, 14)
SIMULADOR  = "https://www.asesoriadevisadosglobal.com/cesar-castro.html"

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

# ─── PLANTILLAS ───────────────────────────────────────────────────────────────
EMAILS = [
    {
        "fecha": date(2026, 7, 1),  # HOY — Bienvenida + simulador listo
        "hora": "20:00",
        "asunto": "🏛️ Tu simulador de entrevista está listo — Asesoría Visa Global",
        "cuerpo": f"""Hola César,

Tu asesoría está en marcha y quiero que tengas todo lo que necesitas para llegar a esa entrevista con una seguridad que la mayoría de aplicantes nunca tiene.

Esto no es un proceso genérico. Todo lo que preparamos contigo está basado en tus datos reales del DS-160, en tu cargo como Alcalde de Santa Clara, en tu rol como presidente del COMAGA y en el propósito concreto de tu viaje a Nueva York. No hay plantillas. No hay copiar y pegar.

Lo que la mayoría de asesores hace es darte una lista de preguntas comunes y desearte suerte.
Lo que nosotros hacemos es construirte un simulador personalizado, prepararte respuesta por respuesta para tu caso específico, y estar disponibles para ti hasta el día de la entrevista.

Con 86 visas aprobadas y un método que hemos afinado durante años, sabemos exactamente qué busca el oficial consular y cómo presentar tu perfil para que hable solo.

Tu perfil, César, es excepcionalmente sólido:
• Eres Alcalde en ejercicio — el vínculo de retorno más poderoso que existe
• Tienes ingresos documentados y estables ($4.474/mes)
• Tu viaje tiene un propósito institucional real y verificable
• No tienes familiares en USA ni rechazos previos

Ahora tienes que trabajar esas respuestas hasta que salgan de forma natural.

👉 TU SIMULADOR PERSONALIZADO:
asesoriadevisadosglobal.com/cesar-castro.html

Practícalo todos los días. Empieza por el recorrido completo (Módulos 1 al 8), luego repite solo las preguntas difíciles. En 10-15 minutos diarios estarás más preparado que el 95% de las personas que van a esa entrevista.

📅 Tu entrevista: Martes 14 de julio · 7:30 AM
📍 Embajada EE.UU. · Avigiras E12-170 · Frente al SOLCA

En los próximos días te enviaré recordatorios con los puntos más importantes. Si tienes alguna duda antes, escríbeme directamente:
📱 WhatsApp: +593 98 784 6751

Vamos con todo.

Roberto Acosta
Asesoría Visa Global
www.asesoriadevisadosglobal.com
"""
    },
    {
        "fecha": date(2026, 7, 2),  # Mañana — Primer recordatorio
        "hora": "09:00",
        "asunto": "📚 Primer paso: practica hoy el módulo básico — Asesoría Visa Global",
        "cuerpo": f"""Hola {CLIENTE_NOMBRE},

Hoy es un buen día para hacer tu primer recorrido completo por el simulador.

👉 {SIMULADOR}

Empieza por el "Recorrido completo" — tarda unos 25 minutos. Lee los módulos de aprendizaje (1 y 2), luego revisa tu DS-160 (Módulo 3) y finalmente practica las 5 preguntas básicas.

Las preguntas del nivel básico son las que el oficial SIEMPRE hace:
• ¿Cuál es el propósito de su viaje?
• ¿Cuánto tiempo se va a quedar?
• ¿Dónde se va a hospedar?
• ¿Quién le paga el viaje?
• ¿Tiene familiares en los Estados Unidos?

Responder estas 5 de forma clara y directa ya pone tu caso en buena posición.

Cualquier duda: WhatsApp +593 98 784 6751

Roberto Acosta
Asesoría Visa Global
"""
    },
    {
        "fecha": date(2026, 7, 7),  # 7 días antes
        "hora": "09:00",
        "asunto": "⏰ 1 semana para tu entrevista en la Embajada — Asesoría Visa Global",
        "cuerpo": f"""Hola {CLIENTE_NOMBRE},

Ya falta solo UNA SEMANA para tu entrevista consular en la Embajada de los EE.UU.

📅 CITA: Martes 14 de julio 2026 · 7:30 AM
📍 Dirección: Avigiras E12-170 y Guayacanes, Quito (frente al Hospital SOLCA)
⚠️ LÍMITE para reagendar/cancelar: Viernes 10 de julio, 5:00 AM

Esta semana practica todos los días con tu simulador:
👉 {SIMULADOR}

Las respuestas más importantes que debes tener memorizadas:
• ¿Propósito del viaje? → COMAGA + Comité Cívico Ecuatoriano en Elmhurst, Queens
• ¿Garantía de regreso? → Alcalde en ejercicio, sesiones de cabildo el 6 de agosto
• ¿Primera vez en USA? → Primera oportunidad institucional. Pasaporte vigente desde 2023.

Cualquier pregunta, escríbeme por WhatsApp: +593 98 784 6751

Roberto Acosta
Asesoría Visa Global
www.asesoriadevisadosglobal.com
"""
    },
    {
        "fecha": date(2026, 7, 10),  # Día límite reagenda
        "hora": "07:00",
        "asunto": "🚨 HOY es el límite para reagendar — Entrevista 14 julio · Asesoría Visa Global",
        "cuerpo": f"""Hola {CLIENTE_NOMBRE},

HOY a las 5:00 AM venció el plazo para cancelar o reprogramar tu cita.

Esto significa que tu entrevista está CONFIRMADA para:
📅 Martes 14 de julio 2026 · 7:30 AM
📍 Embajada EE.UU. · Avigiras E12-170 · Frente al SOLCA

✅ DOCUMENTOS — verifica que los tienes listos:
• Pasaporte original A9905551 (válido hasta jul 2033)
• Hoja de confirmación de cita (este papel)
• Hoja de confirmación DS-160 (código: AA00FMXHFP)
• Nombramiento como Alcalde del GAD Municipal de Santa Clara
• Extractos bancarios últimos 3 meses (salario $4.474/mes)
• Información del Comité Cívico Ecuatoriano si tienes carta de ellos

Sigue practicando:
👉 {SIMULADOR}

Cualquier duda: WhatsApp +593 98 784 6751

Roberto Acosta
Asesoría Visa Global
"""
    },
    {
        "fecha": date(2026, 7, 11),  # 3 días antes
        "hora": "09:00",
        "asunto": "📋 3 días para tu entrevista — Checklist de documentos · Asesoría Visa Global",
        "cuerpo": f"""Hola {CLIENTE_NOMBRE},

En 3 días es tu entrevista. Esta semana practica las preguntas difíciles:

❓ "¿Por qué nunca viajó antes a USA?"
→ "Esta es la primera oportunidad institucional para representar al COMAGA en Nueva York."

❓ "¿Por qué no conoce el nombre de su contacto?"
→ "El contacto es institucional — el Comité Cívico Ecuatoriano como organización, no una persona individual."

❓ "¿Qué garantía da de que regresará?"
→ "Soy Alcalde en ejercicio. Tengo sesiones de cabildo el 6 de agosto."

Practica con el simulador:
👉 {SIMULADOR}

✅ PREPARACIÓN PARA EL DÍA:
• Llega a las 7:00 AM (no a las 7:30)
• Ropa formal (traje oscuro o camisa formal)
• SIN celular — no pasa el control de seguridad
• Lleva SOLO los documentos necesarios en una carpeta

Roberto Acosta
Asesoría Visa Global · +593 98 784 6751
"""
    },
    {
        "fecha": date(2026, 7, 13),  # Día antes
        "hora": "18:00",
        "asunto": "🏛️ Mañana es tu entrevista — Último repaso · Asesoría Visa Global",
        "cuerpo": f"""Hola {CLIENTE_NOMBRE},

Mañana martes 14 de julio a las 7:30 AM es tu entrevista consular.

Esta noche:
✅ Prepara tu carpeta con todos los documentos
✅ Deja la ropa lista (traje formal)
✅ Pon la alarma a las 6:00 AM

Mañana:
⏰ Sale de casa a las 6:30 AM para llegar a las 7:00
📍 Embajada EE.UU. · Avigiras E12-170 · Frente al SOLCA
🚫 NO lleves celular (no pasa seguridad)

Recuerda: la entrevista dura 2-5 minutos. Sé directo. Responde solo lo que te preguntan.

Tu perfil es muy sólido: eres Alcalde de Santa Clara, presidente del COMAGA, con un propósito institucional verificable. Confía en eso.

Mucho éxito mañana. Cualquier cosa, llámame: +593 98 784 6751

Roberto Acosta
Asesoría Visa Global
"""
    },
    {
        "fecha": date(2026, 7, 14),  # El día
        "hora": "06:30",
        "asunto": "🟢 ¡Hoy es el día! Entrevista 7:30 AM — Con todo, César · Asesoría Visa Global",
        "cuerpo": f"""Hola {CLIENTE_NOMBRE},

Hoy es tu entrevista consular. Estás preparado.

⏰ 7:30 AM · Embajada EE.UU. · Avigiras E12-170 · Frente al SOLCA

Recuerda las 3 respuestas clave:
1. COMAGA + Comité Cívico Ecuatoriano en Elmhurst, Queens
2. Alcalde en ejercicio — cabildo el 6 de agosto
3. Primera oportunidad institucional — pasaporte vigente desde 2023

Sé directo. Sé natural. Confía en tu cargo.

¡Mucho éxito!

Roberto Acosta
Asesoría Visa Global · +593 98 784 6751
"""
    },
]

# ─── ENVÍO ────────────────────────────────────────────────────────────────────
def enviar_email(asunto, cuerpo):
    msg = MIMEMultipart()
    msg["From"]    = "=?utf-8?q?Asesor=C3=ADa_Visa_Global?= <" + GMAIL_USER + ">"
    msg["To"]      = CLIENTE_EMAIL
    msg["Cc"]      = ", ".join(CC_VISIBLES)
    msg["Subject"] = asunto
    msg.attach(MIMEText(cuerpo, "plain", "utf-8"))
    todos_los_destinos = [CLIENTE_EMAIL] + CC_VISIBLES + [BCC_ROBERTO]
    with smtplib.SMTP("smtp.gmail.com", 587) as srv:
        srv.ehlo()
        srv.starttls()
        srv.login(GMAIL_USER, GMAIL_PASSWORD)
        srv.sendmail(GMAIL_USER, todos_los_destinos, msg.as_bytes())
    logging.info(f"Email enviado: {asunto[:60]}")

def verificar_y_enviar():
    hoy  = date.today()
    ahora = datetime.now().strftime("%H:%M")
    for em in EMAILS:
        if em["fecha"] == hoy and em["hora"] == ahora:
            try:
                enviar_email(em["asunto"], em["cuerpo"])
            except Exception as e:
                logging.error(f"Error enviando email: {e}")

# ─── MODO: ENVIAR AHORA (para prueba) ────────────────────────────────────────
def enviar_todos_ahora():
    """Envía todos los emails inmediatamente (solo para prueba)."""
    for em in EMAILS:
        try:
            enviar_email(em["asunto"] + " [TEST]", f"[TEST - programado para {em['fecha']}]\n\n{em['cuerpo']}")
            print(f"✅ Enviado: {em['asunto'][:50]}...")
        except Exception as e:
            print(f"❌ Error: {e}")

# ─── SCHEDULER (corre en loop) ────────────────────────────────────────────────
def iniciar_scheduler():
    schedule.every().minute.do(verificar_y_enviar)
    logging.info("Scheduler iniciado. Emails programados hasta el 14 julio 2026.")
    while date.today() <= ENTREVISTA:
        schedule.run_pending()
        time.sleep(30)
    logging.info("Entrevista pasada. Scheduler detenido.")

def enviar_bienvenida():
    """Envía solo el email de bienvenida ahora."""
    em = next(e for e in EMAILS if e["fecha"] == date(2026, 7, 1))
    try:
        enviar_email(em["asunto"], em["cuerpo"])
        print(f"✅ Email de bienvenida enviado a {CLIENTE_EMAIL}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Verifica que GMAIL_PASSWORD sea un App Password válido")

if __name__ == "__main__":
    print("⚠️ SCHEDULER PAUSADO — recordatorios_castro desactivado por consumo de tokens")
    print("Para reactivar, usa: python recordatorios_castro.py --bienvenida")
    # Commented out to stop automatic email loops
    # import sys
    # if len(sys.argv) > 1 and sys.argv[1] == "--bienvenida":
    #     enviar_bienvenida()
    # elif len(sys.argv) > 1 and sys.argv[1] == "--test":
    #     print("Modo TEST — enviando todos los emails ahora...")
    #     enviar_todos_ahora()
    # else:
    #     print("Iniciando scheduler...")
    #     print("  --bienvenida  = enviar solo el email de bienvenida ahora")
    #     print("  --test        = enviar todos los emails ahora (prueba)")
    #     print("  (sin args)    = iniciar scheduler automatico")
    #     iniciar_scheduler()
