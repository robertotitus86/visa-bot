"""
Modulo para buscar casos de clientes en el CRM via Google Sheets (Apps Script)
"""
import httpx
import os

SHEETS_WEBHOOK = os.getenv(
    "GOOGLE_SHEETS_WEBHOOK",
    "https://script.google.com/macros/s/AKfycbxAxCDZ5laDTvU-dfxvdAmyE0JmWfGrDbMDNIf3S_OVK1o-rEM9Gbvz0qkTsXj-vC4k/exec"
)

# Clientes en preparacion activa — reconocidos directamente
CLIENTES_PREPARACION = {
    "593997119313": {  # Luis Seas
        "Nombre Principal": "Luis Alfonso Seas Quezada",
        "Tipo Visa": "USA B1/B2",
        "Num Viajeros": "4 (familia completa)",
        "Estado": "En preparacion de entrevista consular",
        "Paquete": "Preparacion VIP",
        "Llegada USA": "20 marzo 2027",
        "Cita": "Por confirmar",
        "Pago": "Pagado",
        "Notas": (
            "CASO ESPECIAL - FAMILIA SEAS GUAMAN. "
            "Luis es Alcalde del Canton Yacuambi (GAD), elegido 2023, en proceso de reeleccion. $3250/mes. "
            "Esposa Zoila Ines: propietaria Farmacia Familiar Yacuambi. $1500/mes. "
            "Hijos: Zoe Scarlett (14) y Luis Deoniel (16), estudiantes en Loja. "
            "Hotel reservado: Monreale Express & Studios, Orlando FL. "
            "Viajan 20 al 28 marzo 2027 (8 dias). "
            "PRIMER VIAJE a USA - sin rechazos previos. "
            "PUNTO CRITICO: Luis declaro hermana (Lupe Alexandra) en USA - estatus desconocido - ya tiene respuesta preparada. "
            "Tienen portal personalizado: asesoriadevisadosglobal.com/seas-guaman.html "
            "y simulador con 35 preguntas: asesoriadevisadosglobal.com/familia-seas-guaman.html"
        ),
    },
    "593988229894": {  # Zoila Guaman
        "Nombre Principal": "Zoila Ines Guaman Gonzalez",
        "Tipo Visa": "USA B1/B2",
        "Num Viajeros": "4 (familia completa)",
        "Estado": "En preparacion de entrevista consular",
        "Paquete": "Preparacion VIP",
        "Llegada USA": "20 marzo 2027",
        "Cita": "Por confirmar",
        "Pago": "Pagado",
        "Notas": (
            "CASO ESPECIAL - FAMILIA SEAS GUAMAN (conyuge de Luis Alfonso Seas, Alcalde Yacuambi). "
            "Zoila es propietaria de Farmacia Familiar en Yacuambi. $1500/mes. "
            "Viajan en familia: Luis, Zoila, Zoe (14) y Deoniel (16). "
            "Orlando FL, 20-28 marzo 2027. Hotel Monreale Express. "
            "Sin rechazos previos. Sin familiares en USA. "
            "Portal: asesoriadevisadosglobal.com/seas-guaman.html "
            "Simulador: asesoriadevisadosglobal.com/familia-seas-guaman.html?miembro=zoila"
        ),
    },
}

async def buscar_caso_por_telefono(telefono: str) -> dict | None:
    """
    Busca el caso de un cliente en el CRM por numero de telefono.
    Retorna el caso si existe, None si no.
    """
    tel_limpio = "".join(filter(str.isdigit, telefono))
    if not tel_limpio:
        return None

    # Primero revisar clientes en preparacion activa (hardcodeados)
    if tel_limpio in CLIENTES_PREPARACION:
        return {
            "caso": CLIENTES_PREPARACION[tel_limpio],
            "siguiente_paso": "Reforzar practica del simulador y preparar documentos para entrevista"
        }

    try:
        url = f"{SHEETS_WEBHOOK}?action=buscarPorTelefono&telefono={tel_limpio}"
        async with httpx.AsyncClient(timeout=8) as client:
            resp = await client.get(url)
            data = resp.json()
            if data.get("status") == "ok" and data.get("caso"):
                return {
                    "caso": data["caso"],
                    "siguiente_paso": data.get("siguiente_paso", "")
                }
    except Exception:
        pass

    return None


def construir_contexto_crm(resultado: dict) -> str:
    """
    Convierte el resultado del CRM en texto de contexto para Claude.
    Solo incluye lo que el bot necesita saber — sin datos sensibles.
    """
    if not resultado:
        return ""

    caso  = resultado.get("caso", {})
    sgte  = resultado.get("siguiente_paso", "")

    nombre   = caso.get("Nombre Principal", "")
    estado   = caso.get("Estado", "")
    tipo     = caso.get("Tipo Visa", "")
    viajeros = caso.get("Num Viajeros", "")
    paquete  = caso.get("Paquete", "")
    llegada  = caso.get("Llegada USA", "")
    cita     = caso.get("Cita", "")
    pago     = caso.get("Pago", "")
    notas    = caso.get("Notas", "")

    lineas = [
        "=== CLIENTE CON CASO ACTIVO EN EL SISTEMA ===",
        f"Nombre: {nombre}",
        f"Tipo de visa: {tipo}",
        f"Num. viajeros: {viajeros}",
        f"Estado actual: {estado}",
        f"Paquete contratado: {paquete}",
    ]

    if llegada and llegada != "—":
        lineas.append(f"Llegada estimada USA: {llegada}")

    if cita and cita not in ("Por agendar", "—", ""):
        lineas.append(f"Fecha de cita consular: {cita}")

    if pago and pago != "—":
        lineas.append(f"Estado de pago: {pago}")

    if notas and notas != "—":
        lineas.append(f"Notas del asesor: {notas}")

    if sgte:
        lineas.append(f"Proximo paso para este cliente: {sgte}")

    es_preparacion = "preparacion" in estado.lower() or "preparaci" in estado.lower()

    lineas += [
        "",
        "INSTRUCCIONES PARA ESTE CLIENTE:",
        "- Es un cliente activo — NO intentes venderle nada que ya tiene",
        "- Respondele sobre su caso especifico usando el contexto de arriba",
        "- Usa su nombre para personalizar la respuesta",
        "- NO menciones probabilidades de aprobacion (genera ansiedad)",
        "- SI puedes decirle en que paso esta y que sigue",
        "- SI puedes recordarle documentos o acciones pendientes si las notas lo indican",
        "- Si pregunta algo que no puedes responder con el contexto: 'Roberto te contacta enseguida'",
    ]

    if es_preparacion:
        lineas += [
            "- Este cliente esta en PREPARACION DE ENTREVISTA — responde preguntas de practica",
            "- Puedes ayudarle a repasar respuestas de entrevista consular segun su caso",
            "- Si pregunta sobre el simulador: asesoriadevisadosglobal.com/familia-seas-guaman.html",
            "- Portal completo de su familia: asesoriadevisadosglobal.com/seas-guaman.html",
            "- Las sesiones Zoom con Roberto son el 15 y 29 de junio 2026 a las 7 PM",
            "- Si pregunta que debe decir en la entrevista, usa el contexto de su caso para guiarle",
        ]
    else:
        lineas.append("- SI tiene cita agendada, recomiendale el simulador: asesoriadevisadosglobal.com/simulador.html")

    lineas.append("=== FIN CONTEXTO CRM ===")


    return "\n".join(lineas)
