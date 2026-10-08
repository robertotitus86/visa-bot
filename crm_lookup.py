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
    # Paola Samaniego y Karen Beltran: casos cerrados (31 ago 2026).
    "593939406502": {
        "Nombre Principal": "Lucia Piedad Acosta Intriago",
        "Tipo Visa": "USA (B1/B2)",
        "Num Viajeros": "1",
        "Cita": "Lunes 19 octubre 2026, 8:00 AM (TENTATIVA, se va a adelantar) - Embajada EE.UU. Quito",
        "Estado": "Cita tentativa, en preparacion de entrevista",
        "Notas": (
            "Soltera, nacida 28 feb 1980 en Portoviejo, vive en Portoviejo. Trabaja en AME (Quito), talento humano, $2,418/mes; antes 21 anos en Coord. Zonal 4 Salud (2005-feb 2026). Viaje: conferencia ICMA, Long Beach, 16-22 oct 2026, hotel La Quinta Hawaiian Gardens, contacto Sergio Arredondo (ICMA). PUNTO CRITICO: 2 hijos residentes permanentes (LPR) en EE.UU. DS-160 AA00FU4AH1, pasaporte B0495916 (vence 27 ene 2035). DS-160: quien paga en blanco, dice sin estudios secundarios, sin viajes en 5 anos. Primera vez USA, sin rechazos. Tel +593 939406502. Correo luciapiedad.acosta@gmail.com. Simulador: asesoriadevisadosglobal.com/lucia-acosta.html"
        ),
    },
    "593988484970": {
        "Nombre Principal": "Freddy Wilfrido Vasconez Freire",
        "Tipo Visa": "USA (B1/B2)",
        "Num Viajeros": "1",
        "Cita": "Lunes 9 noviembre 2026, 9:00 AM - Embajada EE.UU. Quito (Avigiras E12-170 y Guayacanes)",
        "Estado": "Cita confirmada, en preparacion de entrevista",
        "Notas": (
            "Divorciado (mutuo acuerdo, mar 2011), nacido 9 abr 1965 en Ambato. Cedula 1708764632. Vive y trabaja en Ibarra (Rafael Larrea 3-59 y Simon Bolivar). Ocupacion: confeccion/reparacion de calzado y articulos de cuero, $3,000/mes, cuenta propia. PUNTO CRITICO: el DS-160 dice 'ARTIST/PERFORMER' porque es ARTESANO (calzado y cuero) y esa fue la categoria mas cercana — explicarlo siempre igual. Motivo del viaje: turismo. Estudios: Administracion Aduanera, Liceo Aduanero Ibarra 2011-2013. PRIMER VIAJE a USA, sin rechazos, sin familiares en USA. Unico viaje previo (5 anos): Colombia. Pasaporte B1032986 (nuevo, 3 oct 2025, vence 3 oct 2035). DS-160: AA00FTWGBH. Viaje: turismo B1/B2, 6 dias desde 10 feb 2027, Miami, Days Inn by Wyndham Miami Airport (4767 NW 36th St, Miami Springs FL). Viaja solo, paga el mismo, sin contacto personal en USA. Facebook @FREDDY VASCONEZ. Correo freddyvasc@hotmail.com. Tel +593 98 848 4970. Simulador: asesoriadevisadosglobal.com/freddy-vasconez.html"
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
