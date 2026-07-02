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
    "593992564507": {  # Cesar Castro
        "Nombre Principal": "Romulo Cesar Castro Wilcapi",
        "Tipo Visa": "USA B1/B2",
        "Num Viajeros": "1",
        "Estado": "En preparacion de entrevista consular",
        "Paquete": "Preparacion VIP",
        "Llegada USA": "30 julio 2026",
        "Cita": "14 julio 2026, 7:30 AM — Embajada EE.UU. Quito (Avigiras E12-170, frente Hospital SOLCA)",
        "Pago": "Pagado",
        "Notas": (
            "CASO ESPECIAL - CESAR CASTRO - UN SOLO VIAJERO. "
            "Alcalde del GAD Municipal de Santa Clara, Pastaza. Presidente del COMAGA (Consorcio de Municipios Amazonicos y Galalagos). $4474/mes. "
            "Viaja solo del 30 julio al 5 agosto 2026 (6 dias). Nueva York (Queens). "
            "Hospedaje: 38-70 12th St, Long Island City, Queens NY 11101. "
            "Contacto USA: Ecuadorian Civic Committee, 96-09 Roosevelt Ave 2nd Floor, Elmhurst NY 11368. "
            "DS-160: AA00FMXHFP. Pasaporte A9905551, vence jul 2033. "
            "PRIMER VIAJE a USA - sin rechazos previos. Sin familiares en USA. Esposa en Ecuador: Rocio Rubio Lopez. "
            "PUNTO CRITICO: Primera vez en USA + contacto es organizacion no persona (DO NOT KNOW en DS-160) - tiene respuestas preparadas. "
            "Simulador personalizado: asesoriadevisadosglobal.com/cesar-castro.html"
        ),
    },
    "593985926007": {  # Paul Fernando Rodriguez Narvaez
        "Nombre Principal": "Paul Fernando Rodriguez Narvaez",
        "Tipo Visa": "USA B1/B2",
        "Num Viajeros": "4 (familia completa)",
        "Estado": "En preparacion de entrevista consular",
        "Paquete": "Preparacion VIP",
        "Llegada USA": "21 marzo 2027",
        "Cita": "31 julio 2026, 8:30 AM — Consulado Quito (frente Hospital SOLCA)",
        "Pago": "Pagado",
        "Notas": (
            "CASO ESPECIAL - FAMILIA RODRIGUEZ MASACHE - SEGUNDA SOLICITUD. "
            "Los 4 miembros recibieron negativa 214(b) en noviembre 2025. "
            "Paul Fernando es Alcalde del Canton Paquisha (GAD Municipal), en campana de reeleccion. $4.508/mes. "
            "Ex-Policia Nacional 15 anos (2003-2018). Viajes previos: Espana y Peru. "
            "Conviviente Jenny Enid: Granja Familiar 'El Piolin' (porcina) + Presidenta del Patronato de Accion Social de Paquisha (cargo nuevo desde la negativa). $1.500/mes. "
            "Hijos: Mileidy Maily (19, bachillerato) y Paul Smith (12), estudiantes en Unidad Educativa Soberania Nacional, Paquisha. "
            "Hotel reservado: The Point Hotel & Suites, Orlando FL (7389 Universal Boulevard). "
            "Viajan 21 al 28 marzo 2027 (8 dias). "
            "CAMBIO CLAVE DESDE LA NEGATIVA: campana de reeleccion de Paul Fernando + presidencia del Patronato de Jenny. "
            "Tienen portal personalizado: asesoriadevisadosglobal.com/rodriguez-masache.html "
            "y simulador con 36 preguntas: asesoriadevisadosglobal.com/familia-rodriguez-masache.html"
        ),
    },
    "593991468488": {  # Jenny Enid Masache Yaruqui
        "Nombre Principal": "Jenny Enid Masache Yaruqui",
        "Tipo Visa": "USA B1/B2",
        "Num Viajeros": "4 (familia completa)",
        "Estado": "En preparacion de entrevista consular",
        "Paquete": "Preparacion VIP",
        "Llegada USA": "21 marzo 2027",
        "Cita": "31 julio 2026, 8:30 AM — Consulado Quito (frente Hospital SOLCA)",
        "Pago": "Pagado",
        "Notas": (
            "CASO ESPECIAL - FAMILIA RODRIGUEZ MASACHE (conviviente de Paul Fernando Rodriguez, Alcalde Paquisha) - SEGUNDA SOLICITUD. "
            "Los 4 miembros recibieron negativa 214(b) en noviembre 2025. "
            "Jenny administra la Granja Familiar 'El Piolin' (porcina) en Paquisha y es Presidenta del Patronato de Accion Social del Canton Paquisha — cargo nuevo asumido desde la negativa. $1.500/mes. "
            "Viajan en familia: Paul Fernando, Jenny, Mileidy (19) y Paul Smith (12). "
            "Orlando FL, 21-28 marzo 2027. Hotel The Point Hotel & Suites. "
            "Sin familiares en USA. "
            "Portal: asesoriadevisadosglobal.com/rodriguez-masache.html "
            "Simulador: asesoriadevisadosglobal.com/familia-rodriguez-masache.html?miembro=jenny"
        ),
    },
    "593979521411": {  # Mileidy Maily Masache Yaruqui
        "Nombre Principal": "Mileidy Maily Masache Yaruqui",
        "Tipo Visa": "USA B1/B2",
        "Num Viajeros": "4 (familia completa)",
        "Estado": "En preparacion de entrevista consular",
        "Paquete": "Preparacion VIP",
        "Llegada USA": "21 marzo 2027",
        "Cita": "31 julio 2026, 8:30 AM — Consulado Quito (frente Hospital SOLCA)",
        "Pago": "Pagado",
        "Notas": (
            "CASO ESPECIAL - FAMILIA RODRIGUEZ MASACHE (hija de Paul Fernando Rodriguez y Jenny Masache) - SEGUNDA SOLICITUD. "
            "Los 4 miembros recibieron negativa 214(b) en noviembre 2025. "
            "Mileidy tiene 19 anos, estudiante de Bachillerato en la Unidad Educativa Soberania Nacional, Paquisha. "
            "Viajan en familia: Paul Fernando, Jenny, Mileidy y Paul Smith (12). "
            "Orlando FL, 21-28 marzo 2027. Hotel The Point Hotel & Suites. "
            "Sin familiares en USA. Sin viajes previos. "
            "Portal: asesoriadevisadosglobal.com/rodriguez-masache.html "
            "Simulador: asesoriadevisadosglobal.com/familia-rodriguez-masache.html?miembro=mileidy"
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
