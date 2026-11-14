"""
Genera pdf-tatiana-witt.pdf -- Guia personalizada + checklist + preguntas
Visa B1/B2 USA -- Tatiana Patricia Witt Espinosa
Cita: PENDIENTE de asignacion por el consulado (DS-160 enviado 21-ago-2026)
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

CLIENTE = "Tatiana Witt"
CLIENTE_COMPLETO = "Tatiana Patricia Witt Espinosa"
DESTINO = "Miami, EE.UU."
FECHA_CITA = "16 nov 2026, 08:00"
LUGAR_CITA = "Embajada de EE.UU. en Quito"
DS160 = "AA00FVN0IR"
PASAPORTE = "A8243688"

OUT_PATH = os.path.join(os.path.dirname(__file__), "pdf-tatiana-witt.pdf")

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
    canvas.drawCentredString(cx, cy - 7 * mm, "DE 10")

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
        f"<font size=12 color='#1E293B'><b>{FECHA_CITA}</b></font><br/>"
        f"<font size=9 color='#475569'>{LUGAR_CITA}</font>",
        ParagraphStyle("box", parent=style_body, leading=14, spaceAfter=0)
    )
    right = Paragraph(
        "<font size=8 color='#C2410C'><b>DS-160 / PASAPORTE</b></font><br/>"
        f"<font size=12 color='#1E293B'><b>{DS160}</b></font><br/>"
        f"<font size=9 color='#475569'>{PASAPORTE} · vence 14 sep 2032</font>",
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
        "<font color='#FFFFFF' size=13><b>Gracias por confiar tu proceso en nosotros, Tatiana.</b></font><br/>"
        "<font color='#94A3B8' size=9>Tu cita: lunes 16 de noviembre, 8:00 AM — practica cada día y escríbenos por WhatsApp ante cualquier duda.</font>",
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
    ('¿A qué se dedica usted?', 'Tu cargo según la carta y tu certificado laboral: Asesor 4 de AME. Dilo con ese título y luego explica tus funciones.', 'Soy Asesor 4 de la Asociación de Municipalidades Ecuatorianas, AME, y brindo asesoría técnica a la presidencia. Preparo informes, coordino la agenda presidencial y doy seguimiento a compromisos institucionales.'),
    ('¿Cuánto tiempo se va a quedar?', 'Tres noches: del 3 al 6 de diciembre.', 'Tres noches. Llego el 3 de diciembre y regreso a Ecuador el 6 de diciembre.'),
    ('¿Dónde se va a hospedar?', 'Dirección del DS-160: 50301 Northwest 36th Street, Miami Springs. Ten el nombre del hotel y tu reserva a mano.', 'En la dirección que declaré en mi solicitud, en Miami Springs, Florida. Tengo mi reserva para las tres noches.'),
]

INTERMEDIAS = [
    ('¿Quién paga su viaje?', 'AME, tu empleador, cubre el viaje (aunque el DS-160 no lo muestre). Dilo sin dudar y ten a mano la carta de AME. La inscripción al workshop cuesta $500 por persona: ten claro quién la paga y el comprobante.', 'Mi empleador, AME, cubre los gastos de mi viaje.'),
    ('¿Cuánto gana usted al mes?', '$2,418 mensuales, exactos como en el DS-160.', 'Dos mil cuatrocientos dieciocho dólares mensuales, como asesora técnica en AME.'),
    ('¿Desde cuándo trabaja en AME y dónde trabajaba antes?', 'Antes: Banco de Desarrollo (feb-nov 2025) y CONAFIPS (sep 2020-ene 2025). Ingresaste a AME el 1 de diciembre de 2025.', 'Fui Gerente General de CONAFIPS de 2020 a enero de 2025, luego Gerente de Productos y Programas del Banco de Desarrollo hasta noviembre de 2025, y desde el 1 de diciembre de 2025 asesoro a la presidencia de AME.'),
    ('¿Por qué dejó la gerencia general de CONAFIPS y hoy es asesora?', 'Pregunta probable por el cambio de cargo. Respuesta breve, verdadera y sin críticas a nadie.', 'Cumplí mi periodo en CONAFIPS y luego pasé al Banco de Desarrollo. Hoy aporto mi experiencia asesorando a la presidencia de AME en gobernanza municipal y cooperación internacional.'),
    ('¿Es la primera vez que va a Estados Unidos? ¿Le han negado alguna visa?', 'Primer viaje, nunca ha tenido visa, sin rechazos.', 'Sí, es la primera vez que solicito visa y que viajaría a Estados Unidos. No me han negado ninguna visa.'),
    ('¿Ha viajado antes fuera de Ecuador?', 'Sí: Guatemala, Brasil, República Dominicana, Colombia, Perú y Argentina. Cítalos tal cual están en el DS-160.', 'Sí. En los últimos cinco años viajé a Guatemala, Brasil, República Dominicana, Colombia, Perú y Argentina, y siempre regresé a Ecuador.'),
    ('¿Qué estudió usted?', 'Cuatro estudios. Dilos en orden; el MBA y la maestría fueron en línea.', 'Soy economista por la PUCE. También hice un diplomado en Tributación en la UTPL, un MBA y una maestría en Cooperación Internacional, estos dos últimos en línea.'),
]

DIFICILES = [
    ('Usted fue Gerente General de CONAFIPS. ¿Por qué ahora viaja a un evento y qué beneficio tiene para AME?', 'Conecta el evento con tu cargo: gobernanza municipal y cooperación internacional. Ten el programa a mano.', 'Mi trabajo en AME incluye gobernanza municipal y cooperación internacional. En el workshop sobre comunicación y manejo de crisis para gobiernos conoceré experiencias de otros países y traeré lo aprendido a la institución.'),
    ('Su solicitud dice que hizo un MBA en Andorra y una maestría en Perú. ¿Viajó para estudiarlos?', 'Fueron en línea. Dilo claro y sin dudar: nunca viajaste a Andorra ni a Perú para estudiarlos.', 'No, fueron programas en línea. Los cursé desde Ecuador mientras trabajaba.'),
    ('¿Quién es Jaime Narváez y qué relación tiene con usted?', 'Es tu contacto en EE.UU. según el DS-160 (socio de negocios). Es el Presidente Ejecutivo del Comité Internacional de la Cumbre Latinoamericana de New York y firma tu carta de invitación. Ten claro cómo lo conoces.', 'El señor Jaime Narváez es el Presidente Ejecutivo del comité que organiza el workshop y firmó mi carta de invitación. Lo conozco por el trabajo.'),
    ('¿Qué va a hacer exactamente en ese evento en Miami?', 'Explica el valor para tu cargo, con detalles del programa. Ten la invitación o inscripción a mano.', 'Voy a participar en el workshop «Comunicación y manejo de crisis para Gobiernos Municipales y regionales», y a reunirme con otros participantes. Regreso a AME a aplicar lo aprendido.'),
    ('¿Qué garantía tengo de que usted regresará a Ecuador?', 'Tu arraigo: trabajo en AME, esposo, hogar en Quito, padres en Ecuador, viaje corto.', 'Mi trabajo en AME me espera, mi esposo, mi casa y mis padres están en Quito, y el viaje dura tres noches con regreso el 6 de diciembre.'),
    ('Su esposo no viaja con usted. ¿A qué se dedica y está de acuerdo con el viaje?', 'El DS-160 no dice la ocupación de Mauricio. Responde con su ocupación real, corta y verdadera.', 'Mi esposo, Mauricio, se queda en Quito con nuestro hogar. Está de acuerdo con el viaje y yo regreso el 6 de diciembre.'),
]

TRAMPA = [
    ('¿Ha sufrido daños, violencia o maltrato en su país de origen o en su última residencia habitual?', 'CRÍTICA — pregunta obligatoria 2026 para detectar posibles solicitantes de asilo. Un «sí» puede derivar en negativa automática. Responde con seguridad.', 'No, nunca he sufrido daños, violencia ni maltrato en Ecuador. Vivo y trabajo con normalidad en mi país.'),
    ('¿Teme sufrir daños, persecución o maltrato si regresa a ese país?', 'CRÍTICA — segunda pregunta obligatoria 2026. No tienes motivo real para temer volver.', 'No, no tengo ningún temor de regresar a Ecuador. Es mi país, donde vivo y trabajo.'),
    ('Usted ocupó cargos importantes y hoy gana $2,418. ¿Cómo se paga este viaje?', 'Responde con calma: AME cubre el viaje. Ten la carta de AME a mano.', 'El viaje lo cubre AME, mi empleador. Tengo la carta que lo respalda y mi trabajo me espera a mi regreso.'),
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
        "<b>Jaime Narváez</b>, del Comité Int Cumbre de New York. Tu hospedaje: <b>50301 Northwest 36th Street, Miami Springs, Florida 33166 (dirección del DS-160)</b>. "
        "Es tu primer viaje a Estados Unidos, sin rechazos previos. Trabajas en AME como asesora de la presidencia, tras haber sido Gerente General de CONAFIPS. "
        "<b>Tu entrevista es el lunes 16 de noviembre de 2026, 8:00 AM.</b>", style_body))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("FORTALEZAS DE TU CASO", style_eyebrow))
    story.append(strength_box('', 'Trayectoria de alto nivel en el sector público', 'Gerente General de CONAFIPS (2020-2025) y Gerente de Productos y Programas del Banco de Desarrollo (2025): una carrera sólida y verificable.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Cargo actual en AME', 'Asesoría técnica a la presidencia de AME, con salario declarado de $2,418 mensuales.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Formación sólida y coherente', 'Economía en la PUCE, diplomado en Tributación, MBA y maestría en Cooperación Internacional: todo acorde a tu carrera.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Historial de viajes con retorno', 'En los últimos 5 años viajaste a Guatemala, Brasil, República Dominicana, Colombia, Perú y Argentina, y siempre regresaste a Ecuador.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Arraigo en Ecuador', 'Casada, con tu hogar en Quito, tus padres en Ecuador y sin rechazos previos. Viaje corto de tres noches.'))
    story.append(Spacer(1, 2 * mm))
    story.append(Spacer(1, 3 * mm))
    story.append(CondPageBreak(75 * mm))
    story.append(Paragraph("PUNTOS A PREPARAR CON CALMA", style_eyebrow))
    story.append(risk_box('', 'Primera vez en EE.UU., con viaje de evento', 'Aunque has viajado a otros países, nunca has ido a EE.UU. Lo que más pesa es que el motivo sea claro: qué evento es, quién te invita y qué vas a hacer cada día.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Ingreso reciente a AME y viaje pagado por AME', 'Llevas poco tiempo en AME (desde el 1 de diciembre de 2025) y tu DS-160 dejó en blanco quién paga el viaje. Responde con seguridad que AME lo cubre y ten a mano la carta de AME que lo respalde.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Cambio de cargo: de Gerente General a asesora', 'Pasaste de dirigir CONAFIPS y una gerencia del Banco de Desarrollo a asesorar en AME. El oficial puede preguntar por qué. Prepara una explicación breve y verdadera, y la fecha de ingreso a AME.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Maestrías a distancia en el exterior', 'El MBA de Andorra y la maestría de Tacna (Perú) aparecen en tu DS-160. Ambos fueron en línea: dilo con naturalidad, y ten claro que los cursaste mientras trabajabas, sin salir de Ecuador.'))
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
    bloque_preguntas(story, "NIVEL DIFICIL", "Aquí se decide la entrevista — el punto clave: tu cambio de cargo y tu reciente ingreso a AME",
                     DIFICILES, RED, colors.HexColor("#FFF1F2"))
    story.append(CondPageBreak(90 * mm))

    story.append(Paragraph("MODO OFICIAL CONSULAR", style_eyebrow))
    story.append(Paragraph("Preguntas trampa — practica sin ver la respuesta primero", style_h2))
    story.append(Paragraph("Incluye las 2 preguntas obligatorias 2026 sobre asilo y las de tu cargo y tu reciente ingreso a AME. Responde con calma, sin contradecirte, en 2 o 3 frases.", style_body))
    bloque_preguntas(story, "PREGUNTAS TRAMPA", "El oficial busca inconsistencias — mantén la calma", TRAMPA, RED, REDBG, es_trampa=True)
    story.append(PageBreak())

    story.append(Paragraph("CHECKLIST DE DOCUMENTOS", style_eyebrow))
    story.append(Paragraph("Lo que debes llevar a tu entrevista", style_h2))
    story.append(Spacer(1, 2 * mm))
    story.append(grupo_header("DOCUMENTOS OBLIGATORIOS", "Sin estos no puedes presentarte a la cita", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    obligatorios = [
        ("1", "Pasaporte vigente", f"Número {PASAPORTE}, vence 14 de septiembre de 2032."),
        ("2", "Confirmación DS-160", f"Código de barras legible, número {DS160}."),
        ("3", "Página de confirmación e instrucciones de la cita", "Impresa desde ais.usvisa-info.com, con el código de barras de tu cita (lunes 16 de noviembre de 2026, 8:00 AM)."),
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
        ("7", "Certificado laboral de AME", "Cargo, ingreso el 1 de diciembre de 2025, salario y la autorización de tu viaje al evento."),
        ("8", "Rol de pagos de AME", "Los últimos 3 meses: respalda el salario de $2,418 declarado en el DS-160."),
        ("9", "Certificados de CONAFIPS y del Banco de Desarrollo", "Respaldan tus cargos como Gerente General (2020-2025) y Gerente de Productos y Programas (2025) y la salida de cada uno."),
        ("10", "Estados de cuenta bancarios de 6 meses", "Muestran movimiento coherente con tus ingresos."),
        ("11", "Carta de quien cubre los gastos del viaje", "Carta de AME que diga que AME paga tu viaje y que regresas a tu cargo (el DS-160 dejó en blanco quién paga)."),
        ("12", "Títulos y certificados de tus estudios", "Economía (PUCE), diplomado en Tributación (UTPL), MBA (Andorra) y maestría en Cooperación Internacional (Tacna); el MBA y la maestría, con su modalidad."),
    ]
    for num, titulo, desc in laborales:
        story.append(doc_item(num, titulo, desc, BLUE))
    story.append(Spacer(1, 5 * mm))
    story.append(grupo_header("VIAJE Y RESPALDO ADICIONAL", "Completan tu expediente para la entrevista", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    adicional = [
        ("13", "Carta de invitación al workshop de Miami", "Carta del Comité Internacional de la Cumbre Latinoamericana de New York (30 de octubre de 2026), firmada por Jaime Narváez, Presidente Ejecutivo: workshop del 4 de diciembre en el Hotel Indigo Miami Brickell. Llévala impresa, con el comprobante de la inscripción ($500 por persona) si ya la pagaste."),
        ("14", "Reserva de hospedaje", "Dirección del DS-160: 50301 Northwest 36th Street, Miami Springs — del 3 al 6 de diciembre."),
        ("15", "Itinerario de vuelo (ida y vuelta)", "Con regreso fijo a Ecuador el 6 de diciembre."),
        ("16", "Seguro de viaje / asistencia médica internacional", "Cobertura para todo el periodo del viaje."),
        ("17", "Documentos de arraigo familiar", "Certificado de matrimonio y cédula de tu esposo y de tus padres: solo por si el oficial lo pide."),
    ]
    for num, titulo, desc in adicional:
        story.append(doc_item(num, titulo, desc, GOLD2))
    story.append(PageBreak())

    story.append(Paragraph("ULTIMO PASO", style_eyebrow))
    story.append(Paragraph("El día de tu cita", style_h2))
    story.append(Paragraph(
        "Tu cita es el <b>lunes 16 de noviembre de 2026, 8:00 AM</b> en la Embajada de EE.UU. en Quito (Av. Avigiras E12-170 y Guayacanes, frente al Hospital SOLCA). "
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
    story.append(strength_box("", "Dentro de la entrevista", "Responde solo lo que te preguntan, habla claro y sin apresurarte. Si preguntan por tu cambio de cargo o por tu reciente ingreso a AME, responde con calma y con la verdad: viajas por el evento, tu vida y tu trabajo están en Ecuador, y regresas el 6 de diciembre."))
    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="100%", color=LINE, thickness=1))
    story.append(Spacer(1, 6 * mm))
    story.append(closing_band())
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF generado: {OUT_PATH}")


if __name__ == "__main__":
    build()
