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
    # Todos los casos anteriores cerrados (aprobados) - 4 ago 2026
    "593987672577": {
        "Nombre Principal": "Shirma Consuelo Cortes Sanmiguel",
        "Tipo Visa": "USA (B1/B2)",
        "Num Viajeros": "1",
        "Cita": "13 agosto 2026, 7:30 AM - Consulado Quito (Avigiras E12-170, frente Hospital SOLCA)",
        "Estado": "En preparacion de entrevista consular - confirmar pago tasa MRV",
        "Notas": (
            "Alcaldesa del GAD Municipal de Fco. de Orellana (Coca). Ingreso $4,508/mes. "
            "DS-160: AA00FPKGRL. Pasaporte A9349382 (vence 28 feb 2034). Nacida 29 dic 1973. Soltera. "
            "PRIMER VIAJE A USA. Sin rechazos previos. Sin familiares en USA. "
            "INVITACION OFICIAL de ICLEI (Gobiernos Locales por la Sostenibilidad) a la delegacion de "
            "gobiernos locales en la Semana del Clima de Nueva York (New York Climate Week), 20-27 sept 2026, "
            "en paralelo a la Asamblea General de la ONU. Firmada por Rodrigo de Oliveira Perpetuo, Secretario "
            "Ejecutivo ICLEI America del Sur. Contactos: bianca.cantoni@iclei.org, luz.camacho@iclei.org. "
            "Viaje: 20-28 septiembre 2026, Nueva York. Hospedaje: 891 Amsterdam Avenue, Upper West Side, NY 10025. "
            "Viaja junto a Michelle Revelo (funcionaria de su GAD), a quien designo delegada oficial. "
            "CITA CONSULAR: 13 agosto 2026, 7:30 AM, Consulado Quito. DS-160 firmado 4 agosto 2026. "
            "Simulador: asesoriadevisadosglobal.com/shirma-cortes.html"
        ),
    },
    "593987200130": {
        "Nombre Principal": "Michelle Monserrath Revelo Suarez",
        "Tipo Visa": "USA (B1/B2)",
        "Num Viajeros": "1",
        "Cita": "13 agosto 2026, 7:30 AM - Consulado Quito (Avigiras E12-170, frente Hospital SOLCA)",
        "Estado": "En preparacion de entrevista consular - confirmar pago tasa MRV",
        "Notas": (
            "Jefa de Uso y Ocupacion de Suelo, GAD Municipal de Fco. de Orellana. Ingreso $1,612/mes. "
            "DS-160: AA00FPK3AJ. Pasaporte B1542895 (nuevo, emitido 3 jul 2026, vence 3 jul 2036). "
            "Nacida 18 may 1996 en Quito. Soltera. Maestria en Planificacion y Prospectiva Multisectorial (IAEN); "
            "Ingenieria Geografica y Planificacion Territorial (PUCE Quito). "
            "PRIMER VIAJE A USA. Sin rechazos previos. Sin familiares en USA. "
            "Viaja como DELEGADA OFICIAL designada por la Alcaldesa Shirma Cortes Sanmiguel (su jefa) para "
            "acompanarla a la Semana del Clima de Nueva York (invitacion oficial de ICLEI dirigida a la Alcaldesa, "
            "no a Michelle). Pendiente conseguir memo/oficio formal de designacion del GAD. "
            "Viaje: 20-28 septiembre 2026, Nueva York. Hospedaje: 891 Amsterdam Avenue, Upper West Side, NY 10025. "
            "CITA CONSULAR: 13 agosto 2026, 7:30 AM, Consulado Quito. DS-160 firmado 4 agosto 2026. "
            "Simulador: asesoriadevisadosglobal.com/michelle-revelo.html"
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
