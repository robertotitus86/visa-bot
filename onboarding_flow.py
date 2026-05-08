"""
Secuencias automáticas post-pago y seguimiento de leads.
Todo se activa sin intervención de Roberto.
"""
import os
from followup_manager import programar_followup, cancelar_followups_pendientes

PORTAL_BASE = "https://www.asesoriadevisadosglobal.com/portal.html"
ADMIN_PHONE = os.getenv("PHONE_NUMBER", "593994442512")

VISA_URL_MAP = {
    "schengen":    f"{PORTAL_BASE}?visa=schengen",
    "europa":      f"{PORTAL_BASE}?visa=schengen",
    "reino unido": f"{PORTAL_BASE}?visa=uk",
    "uk":          f"{PORTAL_BASE}?visa=uk",
    "rechazo":     f"{PORTAL_BASE}?visa=rechazo",
    "caso rechazo":f"{PORTAL_BASE}?visa=rechazo",
}

def get_portal_url(tipo_visa: str) -> str:
    key = tipo_visa.lower().strip()
    for k, url in VISA_URL_MAP.items():
        if k in key:
            return url
    return PORTAL_BASE  # USA DS-160 es el tab por defecto


# ── MENSAJES POST-PAGO ────────────────────────────────────────────────────────

def mensajes_bienvenida(nombre: str, paquete: str, precio: int, tipo_visa: str = "") -> list[str]:
    """Secuencia inmediata al confirmar el pago."""
    nombre_corto = nombre.split()[0] if nombre else "Hola"
    portal_url   = get_portal_url(tipo_visa)
    return [
        f"Pago confirmado. Bienvenido/a, {nombre_corto}.\n\n"
        f"Tu {paquete} por ${precio} está activo. Soy Roberto y voy a trabajar tu caso personalmente.\n\n"
        f"El proceso de visa tiene altas probabilidades de éxito cuando se hace bien desde el principio — eso es exactamente lo que vamos a hacer.",

        f"El siguiente paso es completar tu expediente.\n\n"
        f"Toma unos 10 minutos. Puedes hacerlo ahora o cuando tengas un momento tranquilo:\n\n"
        f"{portal_url}\n\n"
        f"Completa el formulario con tus datos. Al final podrás subir tus documentos.",

        f"Una vez que envíes el formulario, recibirás confirmación y yo comenzaré a trabajar tu caso.\n\n"
        f"Si tienes alguna duda en el proceso, escríbeme aquí.",
    ]


def mensaje_recordatorio_formulario(nombre: str, horas: int, tipo_visa: str = "") -> str:
    nombre_corto = nombre.split()[0] if nombre else "Hola"
    portal_url   = get_portal_url(tipo_visa)
    if horas == 24:
        return (
            f"Hola {nombre_corto}, quería recordarte que tu expediente está pendiente.\n\n"
            f"Sin los datos no puedo comenzar a trabajar tu caso. Solo toma 10 minutos:\n\n"
            f"{portal_url}"
        )
    return (
        f"{nombre_corto}, es el último recordatorio sobre tu expediente.\n\n"
        f"Si tienes algún problema para completarlo o prefieres que lo hagamos juntos, dime y coordinamos.\n\n"
        f"{portal_url}"
    )


def mensaje_confirmacion_expediente(nombre: str) -> str:
    nombre_corto = nombre.split()[0] if nombre else "Hola"
    return (
        f"Expediente recibido. Gracias, {nombre_corto}.\n\n"
        f"Voy a revisar toda tu documentación y me pongo en contacto contigo en las próximas 24 horas con el plan de acción para tu visa."
    )


def notificacion_venta_admin(nombre: str, telefono: str, paquete: str, precio: int, tipo_visa: str) -> str:
    return (
        f"VENTA CERRADA\n"
        f"{'─' * 30}\n"
        f"Cliente: {nombre}\n"
        f"Tel: +{telefono}\n"
        f"Servicio: {tipo_visa}\n"
        f"Paquete: {paquete} — ${precio}\n"
        f"Estado: Pago confirmado. Esperando expediente."
    )


# ── MENSAJES FOLLOW-UP DE LEADS (no han pagado) ───────────────────────────────

FOLLOWUP_LEAD = {
    "2h": (
        "Hola, ¿pudiste revisar la información sobre tu visa?\n\n"
        "Estoy aquí si tienes alguna duda. Un diagnóstico de tu caso es gratis y sin compromiso."
    ),
    "24h": (
        "Entiendo que el día a día no da mucho tiempo.\n\n"
        "Cuando tengas 5 minutos, cuéntame qué visa necesitas y te digo exactamente qué tienes que hacer según tu situación."
    ),
    "72h": (
        "No te molesto más después de este mensaje.\n\n"
        "Si en algún momento decides tramitar tu visa, aquí estaré. Los casos que se preparan bien desde el principio tienen el doble de probabilidades de aprobación.\n\n"
        "Éxitos."
    ),
}

# Secuencia para leads CALIENTES: preguntaron precio, mostraron interés real
FOLLOWUP_CALIENTE = {
    "3h": (
        "Oye, me quedé pensando en tu caso.\n\n"
        "Para el perfil que me describiste hay cosas concretas que se pueden hacer para maximizar las probabilidades. ¿Quieres que te cuente cuáles son?"
    ),
    "24h": (
        "Todavía tengo cupo disponible esta semana.\n\n"
        "Si decides avanzar hoy, arrancamos el mismo día. No hay pasos complicados, en 15 minutos ya tendríamos todo lo que necesito de ti.\n\n"
        "¿Qué te frenó?"
    ),
    "72h": (
        "Las citas consulares para este mes se están llenando rápido.\n\n"
        "Si tu viaje es antes de fin de año, el tiempo está justo. ¿Quieres que revisemos juntos si llegas cómodo con los plazos?"
    ),
    "7d": (
        "Hola, última vez que te escribo.\n\n"
        "Si sigues pensando en tramitar tu visa, el proceso mínimo toma entre 4 y 8 semanas. Si arrancas esta semana, todavía llegas bien para la mayoría de destinos.\n\n"
        "Una evaluación de tu caso es gratis. Sin compromiso."
    ),
}


# ── MENSAJES POST-SERVICIO ────────────────────────────────────────────────────

def mensaje_solicitud_testimonio(nombre: str) -> str:
    nombre_corto = nombre.split()[0] if nombre else "Hola"
    return (
        f"Hola {nombre_corto}, espero que todo vaya bien con tu proceso.\n\n"
        f"¿Podrías contarme cómo fue tu experiencia trabajando conmigo? Tu opinión ayuda a más personas a tomar la decisión correcta.\n\n"
        f"Solo una o dos líneas es suficiente."
    )


def mensaje_referido(nombre: str) -> str:
    nombre_corto = nombre.split()[0] if nombre else "Hola"
    return (
        f"Hola {nombre_corto}, ¿cómo estás?\n\n"
        f"Si conoces a alguien que esté pensando en tramitar su visa, me encantaría ayudarle.\n\n"
        f"Por cada persona que nos refieras y contrate el servicio, te envío un bono de $20. Sin límite de referidos."
    )


def mensaje_upsell_6meses(nombre: str) -> str:
    nombre_corto = nombre.split()[0] if nombre else "Hola"
    return (
        f"Hola {nombre_corto}, han pasado unos meses.\n\n"
        f"¿Estás planeando algún otro viaje? Si necesitas otra visa o quieres renovar, recuerda que como cliente anterior tienes prioridad y descuento especial."
    )


# ── ACTIVAR SECUENCIAS ────────────────────────────────────────────────────────

def activar_onboarding_post_pago(telefono: str, nombre: str, paquete: str,
                                  precio: int, tipo_visa: str, phone_number_id: str):
    """
    Programa todos los mensajes automáticos post-pago.
    Los mensajes inmediatos se devuelven para enviar ahora.
    Los recordatorios se programan en Google Sheets.
    """
    # Programar recordatorios de formulario (si no lo completan)
    programar_followup(
        telefono=telefono,
        phone_number_id=phone_number_id,
        tipo="recordatorio_formulario_24h",
        mensaje=mensaje_recordatorio_formulario(nombre, 24, tipo_visa),
        delay_horas=24,
        contexto={"nombre": nombre, "paquete": paquete},
    )
    programar_followup(
        telefono=telefono,
        phone_number_id=phone_number_id,
        tipo="recordatorio_formulario_48h",
        mensaje=mensaje_recordatorio_formulario(nombre, 48, tipo_visa),
        delay_horas=48,
        contexto={"nombre": nombre, "paquete": paquete},
    )
    # Programar post-servicio (30 días después)
    programar_followup(
        telefono=telefono,
        phone_number_id=phone_number_id,
        tipo="solicitud_testimonio",
        mensaje=mensaje_solicitud_testimonio(nombre),
        delay_horas=720,  # 30 días
        contexto={"nombre": nombre},
    )
    programar_followup(
        telefono=telefono,
        phone_number_id=phone_number_id,
        tipo="referido",
        mensaje=mensaje_referido(nombre),
        delay_horas=744,  # 31 días
        contexto={"nombre": nombre},
    )
    programar_followup(
        telefono=telefono,
        phone_number_id=phone_number_id,
        tipo="upsell_6meses",
        mensaje=mensaje_upsell_6meses(nombre),
        delay_horas=4320,  # 6 meses
        contexto={"nombre": nombre},
    )

    return mensajes_bienvenida(nombre, paquete, precio, tipo_visa)


def activar_followup_lead(telefono: str, nombre: str, phone_number_id: str):
    """Secuencia de seguimiento para leads fríos (primer contacto, sin mostrar interés claro)."""
    for delay_key, delay_horas in [("2h", 2), ("24h", 24), ("72h", 72)]:
        programar_followup(
            telefono=telefono,
            phone_number_id=phone_number_id,
            tipo=f"lead_followup_{delay_key}",
            mensaje=FOLLOWUP_LEAD[delay_key],
            delay_horas=delay_horas,
            contexto={"nombre": nombre},
        )


def activar_followup_caliente(telefono: str, nombre: str, phone_number_id: str):
    """
    Secuencia de seguimiento para leads calientes: preguntaron precio,
    mostraron interés real o estuvieron a punto de comprar.
    Cancela la secuencia fría anterior y programa mensajes más directos.
    """
    # Cancelar follow-ups fríos que pudieran estar pendientes
    cancelar_followups_pendientes(telefono, tipo_prefijo="lead_followup")

    for delay_key, delay_horas in [("3h", 3), ("24h", 24), ("72h", 72), ("7d", 168)]:
        programar_followup(
            telefono=telefono,
            phone_number_id=phone_number_id,
            tipo=f"lead_caliente_{delay_key}",
            mensaje=FOLLOWUP_CALIENTE[delay_key],
            delay_horas=delay_horas,
            contexto={"nombre": nombre},
        )


def cancelar_followups_lead(telefono: str):
    """Cancela los follow-ups de lead cuando el cliente ya pagó."""
    cancelar_followups_pendientes(telefono, tipo_prefijo="lead_followup")
