import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


PROMPT_ANALISIS = """Eres un experto en visas con 15 años de experiencia. Analiza los datos del cliente y genera un informe de evaluación conciso.

Datos del cliente:
{datos}

Tipo de visa: {tipo_visa}

Genera un informe con EXACTAMENTE este formato (sin explicaciones extra):

PROBABILIDAD DE APROBACION: [0-100]%

FORTALEZAS:
- [punto 1]
- [punto 2]
- [punto 3 si aplica]

RIESGOS:
- [riesgo 1]
- [riesgo 2 si aplica]

PAQUETE RECOMENDADO: [ESENCIAL $97 / PROFESIONAL $197 / VIP $397]
RAZON: [1 linea explicando por qué ese paquete]

DOCUMENTOS PRIORITARIOS:
- [doc 1]
- [doc 2]
- [doc 3]

NOTA PARA EL ASESOR: [1-2 lineas con observaciones clave del caso]"""


def analizar_cliente(datos: dict, tipo_visa: str, nombre: str) -> str:
    datos_formateados = "\n".join([f"- {k}: {v}" for k, v in datos.items() if v and v != "—"])

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            messages=[{
                "role": "user",
                "content": PROMPT_ANALISIS.format(
                    datos=datos_formateados,
                    tipo_visa=tipo_visa
                )
            }]
        )
        analisis = response.content[0].text

        encabezado = (
            f"🔍 *ANÁLISIS IA — {nombre.upper()}*\n"
            f"{'═' * 35}\n"
            f"Visa: {tipo_visa}\n"
            f"{'═' * 35}\n\n"
        )
        return encabezado + analisis

    except Exception as e:
        return f"⚠️ Error generando análisis: {e}"


def analizar_sesion_completa(personas: list, datos: list, tipo_visa: str) -> list:
    """Genera análisis para cada persona de la sesión. Retorna lista de strings."""
    resultados = []
    for i, nombre in enumerate(personas):
        if i < len(datos):
            analisis = analizar_cliente(datos[i], tipo_visa, nombre)
            resultados.append(analisis)
    return resultados
