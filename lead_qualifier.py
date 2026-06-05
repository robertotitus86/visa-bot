"""
Lead Qualifier — Detecta leads de anuncios Meta y los califica automáticamente.
Cuando el lead es calificado, notifica a Roberto con un resumen y score.
"""
import re
from datetime import datetime

# ── Palabras clave que indican que viene de un anuncio ─────────────────────────
FRASES_ANUNCIO = [
    "vi su anuncio", "vi el anuncio", "vi un anuncio",
    "anuncio de visa", "anuncio de facebook", "vi su publicacion",
    "vi su publicación", "los vi en facebook", "los vi en instagram",
    "quiero evaluar mi caso", "evaluar mi caso de visa",
    "rechazaron la visa", "revertimos", "error que arruina",
    "construimos juntos"
]

# ── Preguntas de calificación ──────────────────────────────────────────────────
CALIFICACION_FLOW = {
    "inicio": {
        "pregunta": (
            "Hola, gracias por escribirnos. Vi que te interesa evaluar tu caso de visa.\n\n"
            "Para ayudarte mejor y que Roberto pueda revisar tu caso hoy mismo, "
            "déjame hacerte 3 preguntas rápidas.\n\n"
            "Primera: ¿qué visa necesitas tramitar?\n"
            "1. Visa USA (americana)\n"
            "2. Visa España o Schengen (Europa)\n"
            "3. Otra\n\n"
            "Escribe el número o el nombre de la visa."
        ),
        "siguiente": "visa"
    },
    "visa": {
        "pregunta": (
            "Perfecto. Segunda pregunta:\n\n"
            "¿Has tenido algún rechazo de visa anteriormente?\n"
            "1. Sí, me rechazaron\n"
            "2. No, es mi primera vez\n"
            "3. No sé / No estoy seguro"
        ),
        "siguiente": "rechazo"
    },
    "rechazo": {
        "pregunta": (
            "Entendido. Última pregunta:\n\n"
            "¿Para cuándo estás pensando en el viaje?\n"
            "1. Menos de 1 mes (urgente)\n"
            "2. Entre 1 y 3 meses\n"
            "3. Más de 3 meses\n"
            "4. Aún no tengo fecha"
        ),
        "siguiente": "tiempo"
    },
    "tiempo": {
        "pregunta": None,  # Fin del flow — procesar y notificar
        "siguiente": None
    }
}

# ── Estado de calificación por número ─────────────────────────────────────────
# {phone: {"paso": "visa", "visa": "USA", "rechazo": "si", "tiempo": None, "notificado": False}}
_estados_calificacion: dict = {}

def viene_de_anuncio(mensaje: str) -> bool:
    """Detecta si el primer mensaje viene de un anuncio de Meta."""
    msg = mensaje.lower().strip()
    return any(frase in msg for frase in FRASES_ANUNCIO)

def es_nuevo_lead(phone: str, mensajes_totales: int) -> bool:
    """True si es uno de los primeros mensajes (posible lead nuevo)."""
    return mensajes_totales <= 2

def iniciar_calificacion(phone: str):
    """Inicia el flow de calificación para un número."""
    _estados_calificacion[phone] = {
        "paso": "inicio",
        "visa": None,
        "rechazo": None,
        "tiempo": None,
        "notificado": False,
        "ts": datetime.now().isoformat()
    }

def esta_en_calificacion(phone: str) -> bool:
    estado = _estados_calificacion.get(phone, {})
    return bool(estado) and not estado.get("notificado", True) and estado.get("paso") in CALIFICACION_FLOW

def obtener_pregunta_actual(phone: str) -> str | None:
    estado = _estados_calificacion.get(phone)
    if not estado:
        return None
    paso = estado["paso"]
    return CALIFICACION_FLOW.get(paso, {}).get("pregunta")

def procesar_respuesta(phone: str, respuesta: str) -> tuple[str | None, bool]:
    """
    Procesa la respuesta del lead y avanza al siguiente paso.
    Retorna (mensaje_siguiente, calificacion_completa)
    """
    estado = _estados_calificacion.get(phone)
    if not estado:
        return None, False

    paso = estado["paso"]
    resp = respuesta.strip().lower()

    # Guardar la respuesta según el paso actual
    if paso == "inicio":
        if "1" in resp or "usa" in resp or "americana" in resp or "americ" in resp:
            estado["visa"] = "Visa USA (B1/B2)"
        elif "2" in resp or "espa" in resp or "schengen" in resp or "europa" in resp:
            estado["visa"] = "Visa España / Schengen"
        elif "3" in resp or "otra" in resp:
            estado["visa"] = "Otra visa"
        else:
            estado["visa"] = respuesta[:50]

    elif paso == "visa":
        if "1" in resp or "si" in resp or "rechaz" in resp or "sí" in resp:
            estado["rechazo"] = "Sí tiene rechazo previo"
        elif "2" in resp or "no" in resp or "primera" in resp:
            estado["rechazo"] = "Primera vez aplicando"
        else:
            estado["rechazo"] = "No sabe / No está seguro"

    elif paso == "rechazo":
        if "1" in resp or "mes" in resp or "urgente" in resp or "urgent" in resp:
            estado["tiempo"] = "Urgente (menos de 1 mes)"
        elif "2" in resp or "tres" in resp or "3" in resp:
            estado["tiempo"] = "1-3 meses"
        elif "3" in resp or "más" in resp or "mas" in resp:
            estado["tiempo"] = "Más de 3 meses"
        else:
            estado["tiempo"] = "Sin fecha definida"

    # Avanzar al siguiente paso
    siguiente = CALIFICACION_FLOW[paso]["siguiente"]
    estado["paso"] = siguiente

    if siguiente and CALIFICACION_FLOW[siguiente]["pregunta"]:
        return CALIFICACION_FLOW[siguiente]["pregunta"], False
    elif siguiente == "tiempo":
        # Aún en el paso "rechazo" - avanzar
        return CALIFICACION_FLOW["rechazo"]["pregunta"], False
    else:
        # Calificación completa
        return None, True

def calcular_score(phone: str) -> dict:
    """Calcula el score del lead y el paquete recomendado."""
    estado = _estados_calificacion.get(phone, {})
    rechazo = estado.get("rechazo", "")
    tiempo = estado.get("tiempo", "")
    visa = estado.get("visa", "")

    # Score base
    score = 50
    nivel = "MEDIO"
    paquete = "Profesional $265"
    urgencia = ""

    # Rechazo previo = lead más caliente (necesita VIP)
    if "sí" in rechazo.lower() or "si" in rechazo.lower():
        score += 30
        paquete = "VIP $320"
        nivel = "ALTO"

    # Urgencia
    if "urgente" in tiempo.lower() or "1 mes" in tiempo.lower():
        score += 20
        urgencia = "URGENTE"
        nivel = "ALTO"
    elif "1-3" in tiempo:
        score += 10
        urgencia = "Esta semana"
    elif "no sabe" in rechazo.lower():
        score -= 10
        nivel = "BAJO"
        paquete = "Esencial $197"

    score = min(100, max(10, score))

    return {
        "score": score,
        "nivel": nivel,
        "paquete": paquete,
        "urgencia": urgencia,
        "visa": visa,
        "rechazo": rechazo,
        "tiempo": tiempo
    }

def generar_notificacion_roberto(phone: str) -> str:
    """Genera el mensaje de alerta para Roberto."""
    data   = calcular_score(phone)
    estado = _estados_calificacion.get(phone, {})

    emojis = {"ALTO": "🔥🔥", "MEDIO": "⚡", "BAJO": "📋"}
    emoji  = emojis.get(data["nivel"], "📋")

    urgencia_txt = f"\nUrgencia:  {data['urgencia']}" if data["urgencia"] else ""

    msg = (
        f"{emoji} LEAD DE ANUNCIO — {data['nivel']}\n\n"
        f"Numero:    +{phone}\n"
        f"Visa:      {data['visa']}\n"
        f"Rechazo:   {data['rechazo']}\n"
        f"Viaja:     {data['tiempo']}"
        f"{urgencia_txt}\n\n"
        f"Score:     {data['score']}/100\n"
        f"Paquete:   {data['paquete']}\n\n"
        f"Responde ahora — el lead esta caliente.\n"
        f"wa.me/{phone}"
    )
    return msg

def mensaje_cierre_calificacion(phone: str) -> str:
    """Mensaje al lead cuando termina la calificación."""
    data = calcular_score(phone)

    if data["nivel"] == "ALTO" or "VIP" in data["paquete"]:
        return (
            "Gracias por la info. Tu caso tiene detalles importantes "
            "que Roberto necesita revisar personalmente.\n\n"
            "Te va a escribir en los próximos minutos para darte "
            "una evaluación honesta y sin compromiso.\n\n"
            "Mientras tanto, ¿tienes alguna duda puntual sobre el proceso?"
        )
    else:
        return (
            "Perfecto, ya tengo tu información.\n\n"
            "Con ese perfil la visa es totalmente posible. "
            "Déjame contarte cómo funciona nuestro proceso "
            "y qué opción se ajusta mejor a tu caso."
        )

def marcar_notificado(phone: str):
    if phone in _estados_calificacion:
        _estados_calificacion[phone]["notificado"] = True
