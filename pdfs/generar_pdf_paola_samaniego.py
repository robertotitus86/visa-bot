"""
Genera pdf-paola-samaniego.pdf -- Guia personalizada + checklist + preguntas
Visa B1/B2 USA -- Jennifer Paola Samaniego Marines
Cita: Jueves 24 de septiembre 2026, 07:30 AM, Embajada EE.UU. Quito
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER

NAVY     = colors.HexColor("#060E1C")
NAVY2    = colors.HexColor("#0F1F38")
GOLD     = colors.HexColor("#F5C842")
GOLD2    = colors.HexColor("#C8861A")
GOLDBG   = colors.HexColor("#FFFBEB")
GREY     = colors.HexColor("#475569")
LIGHTGREY= colors.HexColor("#94A3B8")
DARK     = colors.HexColor("#1E293B")
GREEN    = colors.HexColor("#10B981")
GREENBG  = colors.HexColor("#F0FDF4")
RED      = colors.HexColor("#EF4444")
REDBG    = colors.HexColor("#FEF2F2")
AMBER    = colors.HexColor("#F59E0B")
AMBERBG  = colors.HexColor("#FFF7ED")
BLUE     = colors.HexColor("#3B82F6")
BLUEBG   = colors.HexColor("#EFF6FF")
SLATEBG  = colors.HexColor("#F8FAFC")
LINE     = colors.HexColor("#E2E8F0")

CLIENTE = "Paola Samaniego"
CLIENTE_COMPLETO = "Jennifer Paola Samaniego Marines"
DESTINO = "Nueva York, EE.UU."
FECHA_CITA = "Jueves 24 de septiembre 2026, 7:30 AM (tentativa — gestionando adelantarla)"
LUGAR_CITA = "Embajada de EE.UU. en Quito"
DS160 = "AA00FQMKP1"
PASAPORTE = "A8733853"

OUT_PATH = os.path.join(os.path.dirname(__file__), "pdf-paola-samaniego.pdf")

styles = getSampleStyleSheet()
style_h2 = ParagraphStyle("h2", parent=styles["Normal"], fontName="Helvetica-Bold",
                           fontSize=14, leading=17, textColor=NAVY, spaceBefore=2, spaceAfter=8)
style_eyebrow = ParagraphStyle("eyebrow", parent=styles["Normal"], fontName="Helvetica-Bold",
                                fontSize=8, leading=10, textColor=GOLD2, spaceAfter=4)
style_body = ParagraphStyle("body", parent=styles["Normal"], fontName="Helvetica",
                             fontSize=10, leading=15, textColor=GREY, spaceAfter=6)
style_item_body = ParagraphStyle("item_body", parent=styles["Normal"], fontName="Helvetica",
                                  fontSize=9.5, leading=13.5, textColor=GREY)


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    if canvas.getPageNumber() == 1:
        canvas.saveState()
        canvas.setFillColor(GOLDBG)
        canvas.circle(width - 8 * mm, 70 * mm, 50 * mm, stroke=0, fill=1)
        canvas.setFillColor(SLATEBG)
        canvas.circle(-10 * mm, 30 * mm, 35 * mm, stroke=0, fill=1)
        canvas.restoreState()

    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, 2.5 * mm, height, stroke=0, fill=1)
    canvas.setFillColor(NAVY2)
    canvas.rect(2.5 * mm, 0, 1.5 * mm, height, stroke=0, fill=1)

    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 32 * mm, width, 32 * mm, stroke=0, fill=1)
    canvas.setFillColor(NAVY2)
    canvas.rect(0, height - 32 * mm, width, 4 * mm, stroke=0, fill=1)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(2.2)
    canvas.line(0, height - 32 * mm, width, height - 32 * mm)

    canvas.setFillColor(GOLD)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(20 * mm, height - 13 * mm, "ASESORIA VISA GLOBAL")
    canvas.setFillColor(LIGHTGREY)
    canvas.drawString(20 * mm, height - 18 * mm, "PREPARACION PARA TU ENTREVISTA CONSULAR")

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 17)
    canvas.drawString(20 * mm, height - 27 * mm, f"Visa B1/B2 USA — {CLIENTE}")

    cx, cy = width - 18 * mm, height - 16 * mm
    canvas.setFillColor(GOLD)
    canvas.circle(cx, cy, 9 * mm, stroke=0, fill=1)
    canvas.setFillColor(NAVY)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawCentredString(cx, cy - 2 * mm, str(canvas.getPageNumber()))
    canvas.setFont("Helvetica-Bold", 6.5)
    canvas.drawCentredString(cx, cy - 7 * mm, "DE 6")

    canvas.setFillColor(NAVY2)
    canvas.rect(0, 0, width, 13 * mm, stroke=0, fill=1)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 13 * mm, width, 0.6 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.drawCentredString(width / 2, 8 * mm,
        "Asesoria Visa Global  ·  Roberto Acosta  ·  WhatsApp +593 99 444 2512")
    canvas.setFillColor(GOLD)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawCentredString(width / 2, 4 * mm, "www.asesoriadevisadosglobal.com")
    canvas.restoreState()


def cita_box():
    left = Paragraph(
        "<font size=8 color='#C2410C'><b>CITA CONSULAR</b></font><br/>"
        f"<font size=13 color='#1E293B'><b>{FECHA_CITA}</b></font><br/>"
        f"<font size=9 color='#475569'>{LUGAR_CITA}</font>",
        ParagraphStyle("box", parent=style_body, leading=14, spaceAfter=0)
    )
    right = Paragraph(
        "<font size=8 color='#C2410C'><b>DS-160 / PASAPORTE</b></font><br/>"
        f"<font size=12 color='#1E293B'><b>{DS160}</b></font><br/>"
        f"<font size=9 color='#475569'>{PASAPORTE} · vence 14 abr 2033</font>",
        ParagraphStyle("box2", parent=style_body, leading=14, spaceAfter=0)
    )
    t = Table([[left, right]], colWidths=[100 * mm, 70 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AMBERBG),
        ("BOX", (0, 0), (-1, -1), 1.2, AMBER),
        ("LINEAFTER", (0, 0), (0, 0), 1, colors.HexColor("#FBBF24")),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def strength_box(icono, titulo, desc):
    data = [[Paragraph(
        f"<font size=11>{icono}</font>&nbsp;&nbsp;<b>{titulo}</b><br/>{desc}",
        style_item_body)]]
    t = Table(data, colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GREENBG),
        ("LINEBEFORE", (0, 0), (0, -1), 4, GREEN),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return t


def risk_box(icono, titulo, desc):
    data = [[Paragraph(
        f"<font size=11>{icono}</font>&nbsp;&nbsp;<b>{titulo}</b><br/>{desc}",
        style_item_body)]]
    t = Table(data, colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AMBERBG),
        ("LINEBEFORE", (0, 0), (0, -1), 4, AMBER),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return t


def doc_item(numero, titulo, descripcion, badge_color):
    checkbox = Table([[""]], colWidths=[5.5 * mm], rowHeights=[5.5 * mm],
                      style=TableStyle([("BOX", (0, 0), (-1, -1), 1.1, LIGHTGREY),
                                         ("BACKGROUND", (0, 0), (-1, -1), colors.white)]))
    badge = Table([[Paragraph(f"<b>{numero}</b>", ParagraphStyle(
                    "num", parent=style_body, textColor=colors.white,
                    fontSize=8.5, leading=10, alignment=TA_CENTER))]],
                  colWidths=[10 * mm], rowHeights=[7 * mm],
                  style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), badge_color),
                                     ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                     ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    content = Paragraph(f"<b>{titulo}</b><br/>{descripcion}", style_item_body)
    t = Table([[checkbox, badge, content]], colWidths=[9 * mm, 13 * mm, 148 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
    ]))
    return t


def grupo_header(titulo, subtitulo, color, bg):
    hexcolor = "#%02x%02x%02x" % (int(color.red * 255), int(color.green * 255), int(color.blue * 255))
    text_cell = Paragraph(
        f"<font color='{hexcolor}'><b>{titulo}</b></font>"
        f"<br/><font size=8 color='#475569'>{subtitulo}</font>",
        ParagraphStyle("grupo", parent=style_body, fontSize=12, leading=15, spaceAfter=0))
    t = Table([[text_cell]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 4, color),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def pregunta_card(numero, pregunta, tip, modelo, es_trampa=False):
    color = RED if es_trampa else NAVY2
    bg = REDBG if es_trampa else SLATEBG
    numbadge = Table([[Paragraph(f"<b>{numero}</b>", ParagraphStyle(
            "pnum", parent=style_body, textColor=colors.white,
            fontSize=10, leading=12, alignment=TA_CENTER))]],
          colWidths=[8 * mm], rowHeights=[8 * mm],
          style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), color),
                             ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                             ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    trampa_tag = "<font color='#DC2626'><b>[PREGUNTA TRAMPA] </b></font>" if es_trampa else ""
    content = Paragraph(
        f"{trampa_tag}<b>{pregunta}</b><br/>"
        f"<font color='#94A3B8' size=8.5><i>Tip: {tip}</i></font><br/>"
        f"<font color='#C8861A' size=8><b>RESPUESTA MODELO</b></font><br/>"
        f"<font size=9>{modelo}</font>",
        ParagraphStyle("pq", parent=style_body, fontSize=9.5, leading=13.5, spaceAfter=0))
    t = Table([[numbadge, content]], colWidths=[11 * mm, 159 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.7, (RED if es_trampa else LINE)),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return t


def closing_band():
    data = [[Paragraph(
        "<font color='#F5C842' size=8><b>ASESORIA VISA GLOBAL</b></font><br/>"
        "<font color='#FFFFFF' size=13><b>Gracias por confiar tu proceso en nosotros, Paola.</b></font><br/>"
        "<font color='#94A3B8' size=9>Nos vemos el 24 de septiembre — hasta entonces, "
        "estamos a un mensaje de WhatsApp de distancia.</font>",
        ParagraphStyle("closing", parent=style_body, leading=15, spaceAfter=0))]]
    t = Table(data, colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LINEABOVE", (0, 0), (-1, 0), 2.2, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 14), ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))
    return t


# ───────────────────────────── PREGUNTAS ─────────────────────────────

BASICAS = [
    ("¿Cuál es el propósito de su viaje a Estados Unidos?",
     "Sea directa: viaja a la Semana del Clima de Nueva York por la cooperación AME-ICLEI.",
     "Viajo a Nueva York para participar en la Semana del Clima de Nueva York, como parte de la relación de cooperación internacional que mi institución mantiene con ICLEI, Gobiernos Locales por la Sostenibilidad, del 18 al 28 de septiembre de 2026."),
    ("¿A qué se dedica usted?",
     "Cargo y funcion exacta: Directora Ejecutiva de AME.",
     "Soy la Directora Ejecutiva de la Asociación de Municipalidades Ecuatorianas, AME, en Quito. Dirijo y represento legalmente a la institución y gestiono la cooperación internacional con los gobiernos municipales del país."),
    ("¿Cuánto tiempo se va a quedar?",
     "Fechas exactas del DS-160: 18 al 28 de septiembre.",
     "Diez días. Llego a Nueva York el 18 de septiembre y regreso a Ecuador el 28 de septiembre de 2026."),
    ("¿Dónde se va a hospedar?",
     "507 West 181st Street, Washington Heights, Nueva York.",
     "En el 507 de la calle West 181st, en Washington Heights, Nueva York. Ya tengo la dirección confirmada."),
    ("¿Tiene familiares en los Estados Unidos?",
     "No tiene ningún familiar en USA. Respuesta directa.",
     "No, no tengo ningún familiar en los Estados Unidos."),
]

INTERMEDIAS = [
    ("¿Cuánto gana usted como Directora Ejecutiva de AME?",
     "$4,283 mensuales exactos, según lo declarado en el DS-160.",
     "Cuatro mil doscientos ochenta y tres dólares mensuales, como salario de Directora Ejecutiva de la Asociación de Municipalidades Ecuatorianas."),
    ("¿Qué es ICLEI y cuál es su relación con esa organización?",
     "Red internacional de gobiernos locales por sostenibilidad; usted viaja como asociada de negocios.",
     "ICLEI es una red internacional de gobiernos locales comprometidos con la sostenibilidad urbana. AME mantiene una relación de cooperación institucional con ellos, y viajo como asociada de negocios en representación de mi institución."),
    ("¿Es casada? ¿Su esposo viaja con usted?",
     "Casada con Antonio Menéndez Portilla; él se queda en Ecuador.",
     "Sí, soy casada. Mi esposo se queda en Ecuador — este es un viaje institucional, por mi cargo en AME, y viajo sola."),
    ("¿Ha viajado antes fuera de Ecuador?",
     "Sí, a Colombia en los últimos 5 años.",
     "Sí, he viajado a Colombia en los últimos cinco años, y regresé a Ecuador sin ningún inconveniente."),
    ("¿Es la primera vez que solicita una visa a Estados Unidos?",
     "Sí, primer viaje a USA, sin rechazos previos.",
     "Sí, es mi primera solicitud de visa a Estados Unidos. No tengo rechazos previos de ningún tipo."),
]

DIFICILES = [
    ("Usted lleva muy poco tiempo en su cargo actual — ¿por qué debería creer que es Directora Ejecutiva de AME?",
     "Trayectoria real: 7+ años en contratación pública del sector salud, luego Coordinadora en AME y promoción por perfil técnico.",
     "Tengo más de siete años de trayectoria en gestión de contratación pública, primero en el Ministerio de Salud Pública y luego en AME. Fui promovida a la Dirección Ejecutiva precisamente por ese perfil técnico y esa trayectoria."),
    ("¿Por qué el nombre de su contacto en Estados Unidos aparece como 'no lo conoce'?",
     "El vínculo es institucional (ICLEI como organización), no una persona individual conocida — es honesto, no invente un nombre.",
     "Mi contacto es institucional, con la organización ICLEI, no con una persona en particular que conozca personalmente todavía. Por eso ese campo quedó así en mi solicitud."),
    ("¿Cómo se relaciona la Semana del Clima de Nueva York con AME?",
     "AME agrupa a los municipios del país; la sostenibilidad urbana es parte directa de su gestión institucional.",
     "AME agrupa y representa a los gobiernos municipales del Ecuador, y la sostenibilidad urbana es un tema central de la cooperación internacional que gestionamos. La Semana del Clima de Nueva York es el espacio donde se coordina esa cooperación con ICLEI y otros gobiernos locales."),
    ("¿Qué garantía tengo de que usted regresará a Ecuador?",
     "Cargo ejecutivo, esposo y padres en Ecuador, sin familiares en USA, viaje corto con fecha de regreso fija.",
     "Tengo un cargo de alta responsabilidad institucional en AME al que debo regresar, mi esposo y mis padres viven en Ecuador, y no tengo ningún familiar en Estados Unidos. Mi viaje tiene fecha de regreso fija, el 28 de septiembre."),
    ("¿Quién financia este viaje?",
     "AME cubre el viaje como gasto institucional (vuelos, hospedaje, viáticos) — no es un gasto personal.",
     "El viaje lo cubre la Asociación de Municipalidades Ecuatorianas como gasto institucional, incluyendo vuelos, hospedaje y viáticos, ya que participo en representación oficial de AME."),
]

TRAMPA = [
    ("¿Ha sufrido daños, violencia o maltrato en su país de origen o en su última residencia habitual?",
     "CRÍTICA — pregunta obligatoria 2026 para detectar posibles solicitantes de asilo. Un 'sí' puede derivar en negativa automática.",
     "No, nunca he sufrido daños, violencia ni maltrato en Ecuador. Vivo y trabajo con normalidad en mi país."),
    ("¿Teme sufrir daños, persecución o maltrato si regresa a ese país?",
     "CRÍTICA — segunda pregunta obligatoria 2026. No tiene motivo real para temer volver.",
     "No, no tengo ningún temor de regresar a Ecuador. Es mi país, donde vivo, trabajo y ejerzo mi cargo."),
    ("¿Por qué debería darle la visa a usted y no a cualquier otra persona?",
     "La ley (Sección 214(b)) presume que todo solicitante quiere quedarse — demuéstrelo con hechos, sin sonar a súplica.",
     "Porque tengo un caso sólido y verificable: soy Directora Ejecutiva de AME, viajo por un motivo institucional documentado, y toda mi vida, mi esposo y mi familia están en Ecuador."),
    ("¿Por qué viaja sola y no con su esposo?",
     "Es un viaje institucional por su cargo en AME, no un viaje familiar — responda sin rodeos.",
     "Porque es un viaje de carácter institucional, ligado directamente a mi cargo en AME. Mi esposo se queda en Ecuador; no es un viaje familiar sino de trabajo."),
    ("El evento es una semana, pero su viaje declarado es de diez días — ¿por qué?",
     "Fechas del DS-160 (18-28 sept) incluyen reuniones institucionales antes/después del evento — no invente detalle adicional.",
     "Mi viaje incluye actividades y reuniones institucionales relacionadas con la cooperación de AME, además de la Semana del Clima. Por eso las fechas declaradas son del 18 al 28 de septiembre."),
    ("¿Qué pasaría con su cargo si decide quedarse más tiempo en Estados Unidos?",
     "No contemple esa opción ni siquiera hipotéticamente — reafirme la obligación de regreso.",
     "Eso no es algo que contemple. Mi cargo en AME exige mi regreso puntual, y mi fecha de vuelo de regreso ya está fijada para el 28 de septiembre."),
]


def bloque_preguntas(story, titulo, subtitulo, preguntas, color, bg, es_trampa=False):
    story.append(grupo_header(titulo, subtitulo, color, bg))
    story.append(Spacer(1, 3 * mm))
    for i, (q, tip, modelo) in enumerate(preguntas, 1):
        story.append(pregunta_card(i, q, tip, modelo, es_trampa=es_trampa))
        story.append(Spacer(1, 3 * mm))


def build():
    doc = SimpleDocTemplate(
        OUT_PATH, pagesize=A4,
        topMargin=38 * mm, bottomMargin=24 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm,
        title=f"Visa B1/B2 USA - {CLIENTE}",
    )
    story = []

    # ── PAGINA 1 — Bienvenida + cita + trayecto ────────────────────────
    story.append(Paragraph("TU GUIA PERSONALIZADA", style_eyebrow))
    story.append(Paragraph(f"Hola {CLIENTE.split()[0]}, este es tu plan para llegar lista a tu entrevista", style_h2))
    story.append(Paragraph(
        "En <b>Asesoria Visa Global</b> preparamos contigo cada detalle de tu entrevista consular "
        "para la <b>visa B1/B2</b>. Este documento reune tu guia de preguntas — incluidas las preguntas "
        "trampa del oficial consular — tus fortalezas, tu checklist de documentos y el protocolo del "
        "dia de la cita, todo basado en tu DS-160 real.",
        style_body
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(cita_box())
    story.append(Spacer(1, 8 * mm))

    story.append(Paragraph("TU CASO EN RESUMEN", style_eyebrow))
    story.append(Paragraph("Motivo de viaje: Semana del Clima de Nueva York — delegacion ICLEI", style_h2))
    story.append(Paragraph(
        "Viajas del <b>18 al 28 de septiembre de 2026</b> a Nueva York, como Directora Ejecutiva de la "
        "Asociacion de Municipalidades Ecuatorianas (AME), en el marco de la cooperacion institucional "
        "que AME mantiene con ICLEI — Gobiernos Locales por la Sostenibilidad. Te hospedas en el "
        "507 West 181st Street, Washington Heights, Nueva York.",
        style_body
    ))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("FORTALEZAS DE TU CASO", style_eyebrow))
    story.append(strength_box("✔", "Cargo ejecutivo real y verificable",
        "Directora Ejecutiva de AME, con mas de 7 anos de trayectoria en el sector publico "
        "(Ministerio de Salud Publica 2018-2025, luego AME)."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("✔", "Motivo de viaje institucional documentado",
        "Cooperacion AME-ICLEI para la Semana del Clima de Nueva York — no es un viaje personal ambiguo."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("✔", "Vinculos solidos en Ecuador",
        "Casada, esposo y padres viven en Ecuador. Sin familiares en Estados Unidos, sin rechazos previos."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("✔", "Viaje financiado por AME",
        "Vuelos, hospedaje y viaticos cubiertos por la institucion como gasto institucional, no personal."))
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("PUNTOS A PREPARAR CON CALMA", style_eyebrow))
    story.append(risk_box("⚠", "Ascenso reciente a Direccion Ejecutiva",
        "Tu promocion fue en noviembre 2025, tras 7+ anos de trayectoria en contratacion publica. "
        "Explica el cambio con seguridad, sin sonar improvisada."))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box("⚠", "Contacto en EE.UU. como 'no lo conoce'",
        "El campo quedo asi porque el vinculo es institucional con ICLEI, no con una persona conocida. "
        "Es honesto — no inventes un nombre."))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box("⚠", "Viaja sola, siendo casada",
        "Deja claro que es un viaje de trabajo por tu cargo en AME, no un viaje familiar."))

    story.append(PageBreak())

    # ── PAGINA 2 — Preguntas basicas + intermedias ─────────────────────
    story.append(Paragraph("GUIA DE PREGUNTAS · NIVEL 1 Y 2", style_eyebrow))
    story.append(Paragraph("Preguntas basicas e intermedias con respuesta modelo", style_h2))
    bloque_preguntas(story, "NIVEL BASICO", "Lo primero que suele preguntar el oficial",
                      BASICAS, GREEN, GREENBG)
    story.append(PageBreak())
    bloque_preguntas(story, "NIVEL INTERMEDIO", "Profundiza en tu perfil y tu solvencia",
                      INTERMEDIAS, AMBER, AMBERBG)

    story.append(PageBreak())

    # ── PAGINA 3 — Dificiles + trampa ───────────────────────────────────
    story.append(Paragraph("GUIA DE PREGUNTAS · NIVEL 3", style_eyebrow))
    story.append(Paragraph("Preguntas dificiles — exigen respuestas seguras y sin dudar", style_h2))
    bloque_preguntas(story, "NIVEL DIFICIL", "Aqui es donde se decide la entrevista",
                      DIFICILES, RED, colors.HexColor("#FFF1F2"))

    story.append(PageBreak())

    story.append(Paragraph("MODO OFICIAL CONSULAR", style_eyebrow))
    story.append(Paragraph("Preguntas trampa — practica sin ver la respuesta primero", style_h2))
    story.append(Paragraph(
        "Estas son las preguntas mas dificiles de tu caso, incluidas las 2 preguntas obligatorias "
        "que el gobierno de EE.UU. agrego en 2026 para detectar posibles solicitantes de asilo. "
        "Responde siempre con calma, sin contradecirte, con frases cortas de 2 a 3 oraciones.",
        style_body
    ))
    story.append(Spacer(1, 3 * mm))
    bloque_preguntas(story, "PREGUNTAS TRAMPA", "El oficial busca inconsistencias — manten la calma",
                      TRAMPA, RED, REDBG, es_trampa=True)

    story.append(PageBreak())

    # ── PAGINA 4 — Checklist documentos ─────────────────────────────────
    story.append(Paragraph("CHECKLIST DE DOCUMENTOS", style_eyebrow))
    story.append(Paragraph("Lo que debes llevar a tu entrevista", style_h2))
    story.append(Spacer(1, 2 * mm))
    story.append(grupo_header("DOCUMENTOS OBLIGATORIOS", "Sin estos no puedes presentarte a la cita", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    obligatorios = [
        ("1", "Pasaporte vigente", f"Numero {PASAPORTE}, vence 14 de abril de 2033."),
        ("2", "Confirmacion DS-160", f"Codigo de barras legible, numero {DS160}."),
        ("3", "Pagina de confirmacion e instrucciones de la cita",
         "Impresa desde ais.usvisa-info.com, con el codigo de barras de la cita."),
        ("4", "Fotografia 5x5 cm a color",
         "Tomada dentro de los ultimos 6 meses, fondo claro."),
        ("5", "Comprobante de pago de la tasa MRV",
         "Guardalo impreso — puede ser solicitado en la entrevista."),
        ("6", "Cedula de identidad", "Copia y original, como respaldo adicional de identidad."),
    ]
    for num, titulo, desc in obligatorios:
        story.append(doc_item(num, titulo, desc, GOLD2))
    story.append(Spacer(1, 5 * mm))
    story.append(grupo_header("DOCUMENTOS INSTITUCIONALES DE AME", "Respaldan tu cargo y el motivo del viaje", BLUE, BLUEBG))
    story.append(Spacer(1, 2 * mm))
    institucionales = [
        ("7", "Certificado laboral / nombramiento como Directora Ejecutiva",
         "Emitido por AME, con sello y firma, indicando cargo, funciones y fecha de nombramiento."),
        ("8", "Carta de comision de servicios / autorizacion de viaje institucional",
         "Emitida por AME: autoriza el viaje, confirma que cubre vuelos, hospedaje y viaticos, y detalla el proposito institucional."),
        ("9", "Comunicacion oficial de ICLEI / agenda de la Semana del Clima",
         "Invitacion, programa o agenda oficial de Climate Week NYC que respalde el motivo del viaje."),
        ("10", "3 ultimos roles de pago", "Con sello y firma fisica de AME."),
        ("11", "Tarjetas de presentacion institucionales", "A nombre de AME, con tu cargo de Directora Ejecutiva."),
    ]
    for num, titulo, desc in institucionales:
        story.append(doc_item(num, titulo, desc, BLUE))
    story.append(Spacer(1, 5 * mm))
    story.append(grupo_header("VIAJE Y RESPALDO ADICIONAL", "Completan tu expediente para la entrevista", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    adicional = [
        ("12", "Reserva de alojamiento",
         "507 West 181st Street, Washington Heights, Nueva York, confirmada del 18 al 28 de septiembre."),
        ("13", "Seguro de viaje / asistencia medica internacional",
         "Cobertura para todo el periodo del viaje — buena practica para cualquier viaje institucional al exterior."),
        ("14", "Copia del acta de matrimonio",
         "Refuerza tu vinculo familiar en Ecuador."),
    ]
    for num, titulo, desc in adicional:
        story.append(doc_item(num, titulo, desc, GOLD2))

    story.append(PageBreak())

    # ── PAGINA 5 — Protocolo del dia de la cita ─────────────────────────
    story.append(Paragraph("ULTIMO PASO", style_eyebrow))
    story.append(Paragraph("El dia de tu cita", style_h2))
    story.append(Paragraph(
        f"Tu cita es el <b>{FECHA_CITA}</b> en la {LUGAR_CITA} "
        "(Avigiras E12-170 y Guayacanes, frente al Hospital SOLCA).",
        style_body
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(strength_box("📍", "Llega 20-30 minutos antes",
        "No mas de 15 minutos antes de tu hora exacta — no hay necesidad de llegar mucho antes."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("👔", "Vestimenta formal",
        "Como para una reunion institucional importante — comunica seriedad profesional."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("🎒", "Que llevar",
        "Pasaporte original, confirmacion DS-160 impresa, pagina de confirmacion de cita, "
        "comprobante de pago MRV, foto y documentos de respaldo."))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box("🚫", "Que NO llevar",
        "Celular (no pasa seguridad), laptop, tablet, cables, comida o bebidas."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("💬", "Dentro de la entrevista",
        "Responde solo lo que te preguntan, habla claro y sin apresurarte. Si preguntan por tu "
        "ascenso reciente, explica el cambio una sola vez y sigue adelante — no te justifiques en exceso."))

    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="100%", color=LINE, thickness=1))
    story.append(Spacer(1, 6 * mm))
    story.append(closing_band())

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF generado: {OUT_PATH}")


if __name__ == "__main__":
    build()
