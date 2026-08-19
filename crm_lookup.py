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
    # Shirma Cortes y Michelle Revelo: cita 13 agosto 2026 ya paso — casos cerrados (19 ago 2026).
    "593980881226": {
        "Nombre Principal": "Jennifer Paola Samaniego Marines",
        "Tipo Visa": "USA (B1/B2)",
        "Num Viajeros": "1",
        "Cita": "24 septiembre 2026, 7:30 AM (tentativa, gestionando adelantarla) - Embajada EE.UU. Quito (Avigiras E12-170, frente Hospital SOLCA)",
        "Estado": "En preparacion de entrevista consular",
        "Notas": (
            "Directora Ejecutiva de la Asociacion de Municipalidades Ecuatorianas (AME), Quito. Ingreso $4,283/mes. "
            "7+ anos de trayectoria: Ministerio de Salud Publica (2018-2025), luego AME (ascendida nov 2025). "
            "DS-160: AA00FQMKP1. Pasaporte A8733853 (vence 14 abr 2033). Nacida 8 jun 1984 en Esmeraldas. Casada "
            "con Antonio Menendez Portilla (se queda en Ecuador). Tiene 2 hijos que se quedan en Ecuador: Elheo Amai "
            "Menendez Samaniego (nacido 16 dic 2019, Esmeraldas) y Bruna Alaia Menendez Samaniego (nacida 29 jul 2024, "
            "Esmeraldas). "
            "PRIMER VIAJE A USA. Sin rechazos previos. Sin familiares en USA. "
            "MOTIVO INSTITUCIONAL: cooperacion AME-ICLEI (Gobiernos Locales por la Sostenibilidad) para la "
            "Semana del Clima de Nueva York (Climate Week NYC), climateweeknyc.org. "
            "Contacto USA declarado: ICLEI, Wynkoop 536 Suite 901, Denver CO 80202 (organizacion, no persona - "
            "DO NOT KNOW en DS-160). "
            "Viaje: 18-28 septiembre 2026, Nueva York. Hospedaje: 507 West 181st Street, Washington Heights, NY 10033. "
            "Viaja sola. Viaje financiado por AME como gasto institucional (vuelos, hospedaje, viaticos) - no gasto personal. "
            "CITA CONSULAR: 24 septiembre 2026, 7:30 AM, Embajada EE.UU. Quito — TENTATIVA, se esta gestionando "
            "adelantarla. "
            "Simulador (incluye modo oficial consular con preguntas trampa): asesoriadevisadosglobal.com/paola-samaniego.html"
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
            "- Las notas del asesor (arriba) incluyen el link de su portal y simulador personalizado — usalos para guiarle",
            "- Si pregunta que debe decir en la entrevista, usa el contexto de su caso para guiarle",
        ]
    else:
        lineas.append("- SI tiene cita agendada, recomiendale el simulador: asesoriadevisadosglobal.com/simulador.html")

    lineas.append("=== FIN CONTEXTO CRM ===")


    return "\n".join(lineas)
