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
    # Freddy Vasconez: caso cerrado, visa APROBADA (9 nov 2026).
    "593983503495": {
        "Nombre Principal": "Tatiana Patricia Witt Espinosa",
        "Tipo Visa": "USA (B1/B2)",
        "Num Viajeros": "1",
        "Cita": "Lunes 16 noviembre 2026, 8:00 AM - Embajada EE.UU. Quito (Avigiras E12-170 y Guayacanes)",
        "Estado": "Cita confirmada, en preparacion de entrevista",
        "Notas": (
            "Casada (esposo Mauricio Vicente Maldonado Andrade), nacida 3 oct 1976 en Quito, vive en Pifo/Quito. Trabaja en AME (asesoria tecnica a la presidencia, $2,418/mes); antes Gerente General CONAFIPS (sep 2020-ene 2025) y Gerente de Productos y Programas Banco de Desarrollo (feb-nov 2025). Economista PUCE, diplomado UTPL, MBA Andorra y maestria Tacna. Viaje: workshop de alto nivel 'Comunicacion y manejo de crisis para Gobiernos Municipales y regionales' (4 dic, Hotel Indigo Miami Brickell; inscripcion $500) en Miami, 3-6 dic 2026, direccion 50301 NW 36th St Miami Springs, contacto Jaime Narvaez Pina (Comite Int Cumbre Lat de New York, Hotel Indigo Miami Brickell). DS-160 AA00FVN0IR (firmado 5-nov-2026), pasaporte A8243688 (vence 14 sep 2032). Confirmado por Roberto: ingreso a AME 1-dic-2025, AME paga el viaje (DS-160 en blanco), MBA y maestria en linea. Viajo a Guatemala, Brasil, Rep. Dominicana, Colombia, Peru, Argentina. Primera vez USA, sin rechazos. Cita reagendable hasta 12 nov 5 AM. Tel +593 983503495. Correo witttatiana12@gmail.com. Simulador: asesoriadevisadosglobal.com/tatiana-witt.html"
        ),
    },
    "593939406502": {
        "Nombre Principal": "Lucia Piedad Acosta Intriago",
        "Tipo Visa": "USA (B1/B2)",
        "Num Viajeros": "1",
        "Cita": "Miercoles 18 noviembre 2026, 8:00 AM - Embajada EE.UU. Quito (reagendable hasta 16 nov 5 AM)",
        "Estado": "Cita confirmada, en preparacion de entrevista",
        "Notas": (
            "Soltera, nacida 28 feb 1980 en Portoviejo, vive en Portoviejo. Trabaja en AME (Quito), talento humano, $2,418/mes; antes 21 anos en Coord. Zonal 4 Salud (2005-feb 2026). Viaje (DS-160 NUEVO 30-oct): workshop de alto nivel 'Comunicacion y manejo de crisis para Gobiernos Municipales y regionales' (4 dic, Hotel Indigo Miami Brickell; inscripcion $500) en Miami, 3-6 dic 2026, hospedaje 145 SW 11th St (Hotel Indigo Miami Brickell), contacto Jaime Narvaez Pina (Comite Int Cumbre de New York, Hotel Indigo Miami Brickell). CITA: miercoles 18 nov 2026, 8:00 AM, Embajada Quito, agendada con el DS-160 nuevo AA00FVS4BP (verificado 6 nov 2026). PUNTO CRITICO: 2 hijos residentes permanentes (LPR) en EE.UU. DS-160 AA00FVS4BP, pasaporte B0495916 (vence 27 ene 2035). DS-160: quien paga en blanco; estudios: ing. administracion publica, diplomado UNAM 2022 y maestria Boston 2022-24 ambos VIRTUALES (confirmado por Roberto 30-oct), por eso sin viajes en 5 anos ni nunca en EE.UU.. Primera vez USA, sin rechazos. Tel +593 939406502. Correo luciapiedad.acosta@gmail.com. Simulador: asesoriadevisadosglobal.com/lucia-acosta.html"
        ),
    },
    "593960582993": {
        "Nombre Principal": "Josue Patricio Lopez Telenchana",
        "Tipo Visa": "USA (B1/B2)",
        "Num Viajeros": "1",
        "Cita": "Lunes 23 noviembre 2026, 7:30 AM - Embajada EE.UU. Quito (Avigiras E12-170 y Guayacanes; reagendable hasta 18 nov 5 AM)",
        "Estado": "Cita confirmada, en preparacion de entrevista",
        "Notas": (
            "Soltero, nacido 30 dic 1990 en Quito, vive en Quito. Trabaja en AME dirigiendo cooperacion internacional y relaciones internacionales (ingreso 2023 confirmado por Roberto; cargo exacto no consta en el DS-160), $3,247/mes; antes Director de Cooperacion Internacional del Ministerio de Agricultura y Ganaderia (jul 2017-jul 2021). Estudios: licenciatura en Politica y Estudios Internacionales en Melbourne, Australia (2013-2016) y maestria en Cooperacion Internacional en Univ. Nacional de Seul (ago 2021-dic 2022); habla ingles. Viaje: workshop de alto nivel 'Comunicacion y manejo de crisis para Gobiernos Municipales y regionales' (4 dic, Hotel Indigo Miami Brickell; inscripcion $500) en Miami, 3-6 dic 2026, hospedaje 145 SW 11th St (Hotel Indigo Miami Brickell), contacto Jaime Narvaez Pina (Comite Int Cumbre Lat de New York, Hotel Indigo Miami Brickell). DS-160 AA00FWR9TD (nuevo; reemplaza al AA00FTAIM7, la cita debe quedar con el nuevo) (firmado 11-nov-2026), pasaporte B0577566 (vence 14 mar 2035). Confirmado por Roberto: AME (empleador) paga el viaje (DS-160 en blanco); DS-160 nuevo corrigio Melbourne a Australia. Viajes ultimos 5 anos: Suiza, Brasil, Corea del Sur, Colombia, Paraguay, Panama. Primera vez USA, sin rechazos. Padres en Ecuador. Tel +593 960582993. Correo josue90l@gmail.com. Simulador: asesoriadevisadosglobal.com/josue-lopez.html"
        ),
    },
    "593987308982": {
        "Nombre Principal": "Jorge Cristhian Mora Larrea",
        "Tipo Visa": "USA (B1/B2)",
        "Num Viajeros": "1",
        "Cita": "Lunes 30 noviembre 2026, 8:00 AM - Embajada EE.UU. Quito (Avigiras E12-170 y Guayacanes; reagendable hasta 25 nov 5 AM)",
        "Estado": "Cita confirmada, en preparacion de entrevista",
        "Notas": (
            "Casado (esposa Johanna Elizabeth Peralta Velez), nacido 8 jun 1979 en Tulcan, vive en Quito. Es el VICEMINISTRO DE GOBIERNO del Ecuador (coordina y supervisa gobernaciones e intendencias; $4,283/mes; el DS-160 no trae fecha de ingreso al cargo); el Viceministerio PAGA el viaje (confirmado por Roberto 13-nov); antes Asesor Legislativo en la Asamblea Nacional (ago 2021-may 2025) y asesor juridico y politico en AME (may 2019-jul 2021). Estudios: Derecho UTPL, tecnologo en Politica y Gobierno ILADES, maestria Univ. de Lleida (Espana, VIRTUAL confirmado por Roberto, por eso sin viaje a Espana). Viaje: workshop de alto nivel 'Comunicacion y manejo de crisis para Gobiernos Municipales y regionales' (4 dic) en Miami, 3-6 dic 2026, direccion 5301 NW 36th St, contacto Jaime Narvaez Pina (Comite Int Cumbre Lat de New York, Hotel Indigo Miami Brickell). DS-160 NUEVO AA00FWR8L1 (firmado 13-nov-2026; reemplaza al AA00FWQ991 - la cita debe quedar con el nuevo), pasaporte B1579196 (vence 7 ago 2036). PUNTOS CRITICOS: NEGATIVA 214(b) en 1999 (a los 20 anos), declarada en el DS-160; DS-160 nuevo ya corrigio la direccion de la esposa (misma del hogar); cargo de alto nivel (Viceministro), viaje no oficial B1/B2. Viajes: Colombia y Peru. Primera vez USA. Tel +593 987308982. Correo cristhian.moralarrea@gmail.com. Simulador: asesoriadevisadosglobal.com/cristhian-mora.html"
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
