"""
Genera pdf-josue-lopez.pdf -- Guia personalizada + checklist + preguntas
Visa B1/B2 USA -- Josué Patricio López Telenchana
Cita: lunes 23 nov 2026, 07:30 (DS-160 firmado 11-nov-2026)
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, CondPageBreak
)
from reportlab.lib.enums import TA_CENTER

NAVY     = colors.HexColor("#0A1E5A")
NAVY2    = colors.HexColor("#071A4D")
GOLD     = colors.HexColor("#C9A455")
GOLD2    = colors.HexColor("#B8873A")
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

CLIENTE = "Josué López"
CLIENTE_COMPLETO = "Josué Patricio López Telenchana"
DESTINO = "Miami, EE.UU."
FECHA_CITA = "23 nov 2026, 07:30"
LUGAR_CITA = "Embajada de EE.UU. en Quito"
DS160 = "AA00FTAIM7"
PASAPORTE = "B0577566"

OUT_PATH = os.path.join(os.path.dirname(__file__), "pdf-josue-lopez.pdf")

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
    canvas.drawCentredString(cx, cy - 7 * mm, "DE 9")

    canvas.setFillColor(NAVY2)
    canvas.rect(0, 0, width, 13 * mm, stroke=0, fill=1)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 13 * mm, width, 0.6 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.drawCentredString(width / 2, 8 * mm,
        "Asesoria Visa Global  ·  Roberto Acosta  ·  WhatsApp +593 98 784 6751")
    canvas.setFillColor(GOLD)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawCentredString(width / 2, 4 * mm, "www.asesoriadevisadosglobal.com")
    canvas.restoreState()


def cita_box():
    left = Paragraph(
        "<font size=8 color='#C2410C'><b>CITA CONSULAR</b></font><br/>"
        f"<font size=12 color='#1E293B'><b>{FECHA_CITA}</b></font><br/>"
        f"<font size=9 color='#475569'>{LUGAR_CITA}</font>",
        ParagraphStyle("box", parent=style_body, leading=14, spaceAfter=0)
    )
    right = Paragraph(
        "<font size=8 color='#C2410C'><b>DS-160 / PASAPORTE</b></font><br/>"
        f"<font size=12 color='#1E293B'><b>{DS160}</b></font><br/>"
        f"<font size=9 color='#475569'>{PASAPORTE} · vence 14 mar 2035</font>",
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
        f"<b>{titulo}</b><br/>{desc}",
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
        f"<b>{titulo}</b><br/>{desc}",
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
        f"<font color='#B8873A' size=8><b>RESPUESTA MODELO</b></font><br/>"
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
        "<font color='#C9A455' size=8><b>ASESORIA VISA GLOBAL</b></font><br/>"
        "<font color='#FFFFFF' size=13><b>Gracias por confiar tu proceso en nosotros, Josué.</b></font><br/>"
        "<font color='#94A3B8' size=9>Tu cita: lunes 23 de noviembre, 7:30 AM — practica cada día y escríbenos por WhatsApp ante cualquier duda.</font>",
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
    ('¿Cuál es el propósito de su viaje a Estados Unidos?', 'Workshop de alto nivel en Miami (carta del comité), el 4 de diciembre. Respuesta directa y corta.', 'Viajo a Miami, Florida, tres noches, del 3 al 6 de diciembre, al workshop de alto nivel «Comunicación y manejo de crisis para Gobiernos Municipales y regionales», el 4 de diciembre, organizado por el Comité Internacional de la Cumbre Latinoamericana de New York.'),
    ('¿A qué se dedica usted?', 'Tu cargo según la carta y tu certificado laboral: Director Nacional de Cooperación de AME. Dilo con ese título y luego explica tus funciones.', 'Soy Director Nacional de Cooperación de la Asociación de Municipalidades Ecuatorianas, AME. Dirijo las estrategias de cooperación internacional y las relaciones con cooperantes y organismos multilaterales a favor de los municipios del país.'),
    ('¿Cuánto tiempo se va a quedar?', 'Tres noches: del 3 al 6 de diciembre.', 'Tres noches. Llego el 3 de diciembre y regreso a Ecuador el 6 de diciembre.'),
    ('¿Dónde se va a hospedar?', 'Dirección del DS-160: 5301 Northwest 36th Street, Miami Springs. Ten el nombre del hotel y tu reserva a mano.', 'En la dirección que declaré en mi solicitud, en Miami Springs, Florida. Tengo mi reserva para las tres noches.'),
]

INTERMEDIAS = [
    ('¿Quién paga su viaje?', 'AME, tu empleador, cubre el viaje (aunque el DS-160 no lo muestre). Dilo sin dudar y ten a mano la carta de AME. La inscripción al workshop cuesta $500 por persona: ten claro quién la paga y el comprobante.', 'Mi empleador, la Asociación de Municipalidades Ecuatorianas, AME, cubre los gastos de mi viaje. Tengo la carta que lo respalda.'),
    ('¿Cuánto gana usted al mes?', '$3,247 mensuales, exactos como en el DS-160.', 'Tres mil doscientos cuarenta y siete dólares mensuales en AME.'),
    ('¿Dónde trabajaba antes de AME?', 'Ministerio de Agricultura y Ganadería, Director de Cooperación Internacional (jul 2017 - jul 2021). Ingresaste a AME en 2023.', 'Fui Director de Cooperación Internacional en el Ministerio de Agricultura y Ganadería, de julio de 2017 a julio de 2021. Desde 2023 trabajo en AME en cooperación internacional.'),
    ('¿Es la primera vez que va a Estados Unidos? ¿Le han negado alguna visa?', 'Primer viaje, nunca ha tenido visa, sin rechazos.', 'Sí, es la primera vez que solicito visa y que viajaría a Estados Unidos. No me han negado ninguna visa.'),
    ('¿Ha viajado antes fuera de Ecuador?', 'Sí: Suiza, Brasil, Corea del Sur, Colombia, Paraguay y Panamá. Cítalos tal cual están en el DS-160.', 'Sí. En los últimos cinco años viajé a Suiza, Brasil, Corea del Sur, Colombia, Paraguay y Panamá, y siempre regresé a Ecuador.'),
    ('¿Qué estudió usted?', 'Dos estudios: licenciatura en Melbourne (Australia) y maestría en Seúl (Corea del Sur). Dilos en orden y con fechas.', 'Soy licenciado en Política y Estudios Internacionales por la Universidad de Melbourne, en Australia, y tengo una maestría en Cooperación Internacional de la Universidad Nacional de Seúl, en Corea del Sur.'),
]

DIFICILES = [
    ('Usted dirige cooperación internacional en AME. ¿Qué beneficio tiene este evento para su institución?', 'Conecta el evento con tu cargo: alianzas y cooperación para los municipios. Ten el programa a mano.', 'Mi trabajo en AME es crear alianzas y cooperación para los municipios del país. En el workshop sobre comunicación y manejo de crisis para gobiernos conoceré experiencias y contactos de otros países y traeré lo aprendido a la institución.'),
    ('Su solicitud dice que estudió en Australia y en Corea del Sur. ¿Cuánto tiempo vivió fuera y por qué regresó?', 'Estudiaste fuera y siempre regresaste a Ecuador a trabajar. Responde con fechas exactas: Melbourne 2013-2016, Seúl ago 2021 - dic 2022.', 'Estudié mi licenciatura en Melbourne de 2013 a 2016 y mi maestría en Seúl de agosto de 2021 a diciembre de 2022. Al terminar regresé a Ecuador porque mi familia y mi carrera están aquí.'),
    ('¿Quién es Jaime Narváez y qué relación tiene con usted?', 'Es tu contacto en EE.UU. según el DS-160 (socio de negocios). Es el Presidente Ejecutivo del Comité Internacional de la Cumbre Latinoamericana de New York y firma tu carta de invitación. Ten claro cómo lo conoces.', 'El señor Jaime Narváez es el Presidente Ejecutivo del comité que organiza el workshop y firmó mi carta de invitación. Lo conozco por el trabajo.'),
    ('¿Qué va a hacer exactamente en ese evento en Miami?', 'Explica el valor para tu cargo, con detalles del programa. Ten la invitación o inscripción a mano.', 'Voy a participar en el workshop «Comunicación y manejo de crisis para Gobiernos Municipales y regionales», y a reunirme con otros participantes. Regreso a AME a aplicar lo aprendido.'),
    ('¿Qué garantía tengo de que usted regresará a Ecuador?', 'Tu arraigo: cargo directivo en AME, hogar en Quito, padres en Ecuador, viaje corto y de regreso a tu trabajo.', 'Mi cargo en AME me espera, mi casa y mis padres están en Quito, y el viaje dura tres noches con regreso el 6 de diciembre.'),
    ('Usted estudió en el extranjero y habla inglés. ¿Por qué no se quedó a vivir o trabajar fuera?', 'Responde con calma: tu proyecto profesional está en Ecuador, ya fuiste director en el Ministerio y hoy diriges cooperación en AME.', 'Porque mi carrera y mi familia están en Ecuador. Estudié afuera para prepararme y volví a aplicar lo aprendido, primero en el Ministerio de Agricultura y ahora en AME.'),
]

TRAMPA = [
    ('¿Ha sufrido daños, violencia o maltrato en su país de origen o en su última residencia habitual?', 'CRÍTICA — pregunta obligatoria 2026 para detectar posibles solicitantes de asilo. Un «sí» puede derivar en negativa automática. Responde con seguridad.', 'No, nunca he sufrido daños, violencia ni maltrato en Ecuador. Vivo y trabajo con normalidad en mi país.'),
    ('¿Teme sufrir daños, persecución o maltrato si regresa a ese país?', 'CRÍTICA — segunda pregunta obligatoria 2026. No tienes motivo real para temer volver.', 'No, no tengo ningún temor de regresar a Ecuador. Es mi país, donde vivo y trabajo.'),
    ('Usted estudió dos veces en el extranjero y no tiene hijos ni pareja. ¿Qué le ata a Ecuador?', 'Pregunta trampa de arraigo. No te pongas a la defensiva: trabajo, padres, hogar, carrera.', 'Mi trabajo como responsable de cooperación en AME, mis padres, mi casa en Quito y mi carrera. Voy tres noches al evento y regreso a mi puesto.'),
    ('¿Piensa trabajar o quedarse a vivir en Estados Unidos?', 'No lo contemples ni como hipótesis. Respuesta corta.', 'No. Voy tres noches al evento y regreso a mi trabajo en AME.'),
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
    story.append(Paragraph("TU GUIA PERSONALIZADA", style_eyebrow))
    story.append(Paragraph(f"Hola {CLIENTE.split()[0]}, este es tu plan para llegar listo a tu entrevista", style_h2))
    story.append(Paragraph(
        "En <b>Asesoría Visa Global</b> preparamos contigo cada detalle de tu entrevista consular para la <b>visa B1/B2</b>. "
        "Este documento reúne tu guía de preguntas — incluidas las preguntas trampa del oficial consular — tus fortalezas, "
        "tu checklist de documentos y el protocolo del día de la cita, todo basado en tu DS-160 real.", style_body))
    story.append(Spacer(1, 3 * mm))
    story.append(cita_box())
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("TU CASO EN RESUMEN", style_eyebrow))
    story.append(Paragraph("Motivo de viaje: workshop de alto nivel en Miami, 3 noches", style_h2))
    story.append(Paragraph(
        "Viajas a <b>Miami, Florida</b> del <b>3 al 6 de diciembre de 2026</b> a un workshop de alto nivel; tu contacto es "
        "<b>Jaime Narváez</b>, del Comité Int Cumbre Lat de New York. Tu hospedaje: <b>5301 Northwest 36th Street, Miami Springs, Florida 33166 (dirección del DS-160)</b>. "
        "Es tu primer viaje a Estados Unidos, sin rechazos previos. Trabajas en AME dirigiendo la cooperación internacional, tras haber sido Director de Cooperación Internacional del Ministerio de Agricultura. "
        "<b>Tu entrevista es el lunes 23 de noviembre de 2026, 7:30 AM.</b>", style_body))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("FORTALEZAS DE TU CASO", style_eyebrow))
    story.append(strength_box('', 'Cargo directivo en cooperación internacional', 'Diriges las estrategias de cooperación y las relaciones internacionales de AME a favor de 222 municipios, con salario declarado de $3,247 mensuales.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Trayectoria verificable', 'Director de Cooperación Internacional del Ministerio de Agricultura y Ganadería (2017-2021): una carrera sólida y coherente con tu cargo actual.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Formación coherente', 'Licenciatura en Política y Estudios Internacionales (Melbourne) y maestría en Cooperación Internacional (Seúl): todo acorde a tu carrera. Hablas inglés.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Historial de viajes con retorno', 'En los últimos 5 años viajaste a Suiza, Brasil, Corea del Sur, Colombia, Paraguay y Panamá, y siempre regresaste a Ecuador.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Arraigo en Ecuador', 'Hogar en Quito, padres en Ecuador y sin rechazos previos. Viaje corto de tres noches.'))
    story.append(Spacer(1, 2 * mm))
    story.append(Spacer(1, 3 * mm))
    story.append(CondPageBreak(75 * mm))
    story.append(Paragraph("PUNTOS A PREPARAR CON CALMA", style_eyebrow))
    story.append(risk_box('', 'Primera vez en EE.UU., con viaje de evento', 'Aunque has viajado a otros países, nunca has ido a EE.UU. Lo que más pesa es que el motivo sea claro: qué evento es, quién te invita y qué vas a hacer cada día.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Viaje pagado por AME', 'Tu DS-160 dejó en blanco quién paga el viaje. Responde con seguridad que AME, tu empleador, lo cubre y ten a mano la carta de AME que lo respalde.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Estudios en el exterior y arraigo', 'Estudiaste en Australia y en Corea del Sur, y no tienes pareja ni hijos. El oficial puede preguntar qué te ata a Ecuador: tu cargo en AME, tus padres, tu casa en Quito y tu carrera.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Fechas laborales y de estudio', 'Tu cargo en el Ministerio terminó en julio de 2021, tu maestría en Seúl fue de agosto de 2021 a diciembre de 2022 y entraste a AME en 2023. Ten claros los meses exactos de cada etapa.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Hospedaje y contacto en Miami', 'Tu DS-160 trae una dirección en Miami Springs y un contacto en el Hotel Indigo de Brickell. Ten claro dónde dormirás realmente y cuál es tu relación con Jaime Narváez.'))
    story.append(Spacer(1, 2 * mm))
    story.append(PageBreak())

    story.append(Paragraph("GUIA DE PREGUNTAS · NIVEL 1 Y 2", style_eyebrow))
    story.append(Paragraph("Preguntas básicas e intermedias con respuesta modelo", style_h2))
    bloque_preguntas(story, "NIVEL BASICO", "Lo primero que suele preguntar el oficial", BASICAS, GREEN, GREENBG)
    story.append(CondPageBreak(80 * mm))
    bloque_preguntas(story, "NIVEL INTERMEDIO", "Profundiza en tu perfil y tu solvencia", INTERMEDIAS, AMBER, AMBERBG)
    story.append(CondPageBreak(80 * mm))

    story.append(Paragraph("GUIA DE PREGUNTAS · NIVEL 3", style_eyebrow))
    story.append(Paragraph("Preguntas difíciles — exigen respuestas seguras y sin dudar", style_h2))
    bloque_preguntas(story, "NIVEL DIFICIL", "Aquí se decide la entrevista — el punto clave: el viaje pagado por AME y tu arraigo",
                     DIFICILES, RED, colors.HexColor("#FFF1F2"))
    story.append(CondPageBreak(90 * mm))

    story.append(Paragraph("MODO OFICIAL CONSULAR", style_eyebrow))
    story.append(Paragraph("Preguntas trampa — practica sin ver la respuesta primero", style_h2))
    story.append(Paragraph("Incluye las 2 preguntas obligatorias 2026 sobre asilo y las de el viaje pagado por AME y tu arraigo. Responde con calma, sin contradecirte, en 2 o 3 frases.", style_body))
    bloque_preguntas(story, "PREGUNTAS TRAMPA", "El oficial busca inconsistencias — mantén la calma", TRAMPA, RED, REDBG, es_trampa=True)
    story.append(PageBreak())

    story.append(Paragraph("CHECKLIST DE DOCUMENTOS", style_eyebrow))
    story.append(Paragraph("Lo que debes llevar a tu entrevista", style_h2))
    story.append(Spacer(1, 2 * mm))
    story.append(grupo_header("DOCUMENTOS OBLIGATORIOS", "Sin estos no puedes presentarte a la cita", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    obligatorios = [
        ("1", "Pasaporte vigente", f"Número {PASAPORTE}, vence 14 de marzo de 2035."),
        ("2", "Confirmación DS-160", f"Código de barras legible, número {DS160}."),
        ("3", "Página de confirmación e instrucciones de la cita", "Impresa desde ais.usvisa-info.com, con el código de barras de tu cita (lunes 23 de noviembre de 2026, 7:30 AM)."),
        ("4", "Fotografía 5x5 cm a color", "Tomada dentro de los últimos 6 meses, fondo claro."),
        ("5", "Comprobante de pago de la tasa MRV", "Guárdalo impreso — puede ser solicitado en la entrevista."),
        ("6", "Cédula de identidad", "Original y copia, como respaldo adicional de identidad."),
    ]
    for num, titulo, desc in obligatorios:
        story.append(doc_item(num, titulo, desc, GOLD2))
    story.append(Spacer(1, 5 * mm))
    story.append(grupo_header("DOCUMENTOS DE TRABAJO E INGRESOS", "Respaldan tu cargo en AME y tu trayectoria", BLUE, BLUEBG))
    story.append(Spacer(1, 2 * mm))
    laborales = [
        ("7", "Certificado laboral de AME", "Cargo, ingreso en 2023, salario y la autorización de tu viaje al evento."),
        ("8", "Rol de pagos de AME", "Los últimos 3 meses: respalda el salario de $3,247 declarado en el DS-160."),
        ("9", "Certificado del Ministerio de Agricultura y Ganadería", "Respalda tu cargo como Director de Cooperación Internacional (jul 2017 - jul 2021) y tu salida."),
        ("10", "Estados de cuenta bancarios de 6 meses", "Muestran movimiento coherente con tus ingresos."),
        ("11", "Carta de quien cubre los gastos del viaje", "Carta de AME que diga que AME paga tu viaje y que regresas a tu cargo (el DS-160 dejó en blanco quién paga)."),
        ("12", "Títulos y certificados de tus estudios", "Licenciatura en Política y Estudios Internacionales (Melbourne, 2013-2016) y maestría en Cooperación Internacional (Universidad Nacional de Seúl, 2021-2022)."),
    ]
    for num, titulo, desc in laborales:
        story.append(doc_item(num, titulo, desc, BLUE))
    story.append(Spacer(1, 5 * mm))
    story.append(grupo_header("VIAJE Y RESPALDO ADICIONAL", "Completan tu expediente para la entrevista", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    adicional = [
        ("13", "Carta de invitación al workshop de Miami", "Carta del Comité Internacional de la Cumbre Latinoamericana de New York (30 de octubre de 2026), firmada por Jaime Narváez, Presidente Ejecutivo: workshop del 4 de diciembre en el Hotel Indigo Miami Brickell. Llévala impresa, con el comprobante de la inscripción ($500 por persona) si ya la pagaste."),
        ("14", "Reserva de hospedaje", "Dirección del DS-160: 5301 Northwest 36th Street, Miami Springs — del 3 al 6 de diciembre."),
        ("15", "Itinerario de vuelo (ida y vuelta)", "Con regreso fijo a Ecuador el 6 de diciembre."),
        ("16", "Seguro de viaje / asistencia médica internacional", "Cobertura para todo el periodo del viaje."),
        ("17", "Documentos de arraigo", "Cédula de tus padres y comprobante de tu domicilio en Quito: solo por si el oficial lo pide."),
    ]
    for num, titulo, desc in adicional:
        story.append(doc_item(num, titulo, desc, GOLD2))
    story.append(PageBreak())

    story.append(Paragraph("ULTIMO PASO", style_eyebrow))
    story.append(Paragraph("El día de tu cita", style_h2))
    story.append(Paragraph(
        "Tu cita es el <b>lunes 23 de noviembre de 2026, 7:30 AM</b> en la Embajada de EE.UU. en Quito (Av. Avigiras E12-170 y Guayacanes, frente al Hospital SOLCA). "
        "Lleva la confirmación del DS-160 con el código de barras que corresponde a tu cita y tu pasaporte.", style_body))
    story.append(Spacer(1, 3 * mm))
    story.append(strength_box("", "Llega 20-30 minutos antes", "No más de 15 minutos antes de tu hora exacta de ingreso — no hay necesidad de llegar mucho antes."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("", "Vestimenta formal", "Como para una reunión importante — comunica seriedad."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("", "Qué llevar", "Pasaporte original, confirmación DS-160 impresa, página de confirmación de cita, comprobante de pago MRV, foto y los documentos de respaldo de tu trabajo en AME, de tus estudios y del evento."))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box("", "Qué NO llevar", "Celular (no pasa seguridad), laptop, tablet, cables, comida o bebidas."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("", "Dentro de la entrevista", "Responde solo lo que te preguntan, habla claro y sin apresurarte. Si preguntan por el pago del viaje o por tus estudios en el exterior, responde con calma y con la verdad: viajas por el evento, tu vida y tu trabajo están en Ecuador, y regresas el 6 de diciembre."))
    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="100%", color=LINE, thickness=1))
    story.append(Spacer(1, 6 * mm))
    story.append(closing_band())
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF generado: {OUT_PATH}")


if __name__ == "__main__":
    build()
