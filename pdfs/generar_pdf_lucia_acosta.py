"""
Genera pdf-lucia-acosta.pdf -- Guia personalizada + checklist + preguntas
Visa B1/B2 USA -- Lucía Piedad Acosta Intriago
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

CLIENTE = "Lucía Acosta"
CLIENTE_COMPLETO = "Lucía Piedad Acosta Intriago"
DESTINO = "Miami, EE.UU."
FECHA_CITA = "18 nov 2026, 08:00"
LUGAR_CITA = "Embajada de EE.UU. en Quito"
DS160 = "AA00FVS4BP"
PASAPORTE = "B0495916"

OUT_PATH = os.path.join(os.path.dirname(__file__), "pdf-lucia-acosta.pdf")

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
        f"<font size=9 color='#475569'>{PASAPORTE} · vence 27 ene 2035</font>",
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
        "<font color='#FFFFFF' size=13><b>Gracias por confiar tu proceso en nosotros, Lucía.</b></font><br/>"
        "<font color='#94A3B8' size=9>Tu cita: miércoles 18 de noviembre, 8:00 AM — practica cada día y escríbenos por WhatsApp ante cualquier duda.</font>",
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
    ('¿Cuál es el propósito de su viaje a Estados Unidos?', 'Workshop de alto nivel en Miami (carta del comité), el 4 de diciembre. Respuesta directa..', 'Viajo a Miami, Florida, tres noches, del 3 al 6 de diciembre, al workshop de alto nivel «Comunicación y manejo de crisis para Gobiernos Municipales y regionales», el 4 de diciembre, organizado por el Comité Internacional de la Cumbre Latinoamericana de New York.'),
    ('¿A qué se dedica usted?', 'Tu cargo según la carta y tu certificado laboral: Coordinadora de Talento Humano de AME. Dilo con ese título y luego explica tus funciones.', 'Soy Coordinadora de Talento Humano de la Asociación de Municipalidades Ecuatorianas, AME. Soy responsable de la administración de personal: reclutamiento, contratos y nómina.'),
    ('¿Cuánto tiempo se va a quedar?', 'Tres noches: del 3 al 6 de diciembre.', 'Tres noches. Llego el 3 de diciembre y regreso a Ecuador el 6 de diciembre.'),
    ('¿Dónde se va a hospedar?', 'Dirección del DS-160: 5301 Northwest 36th Street..', 'En la dirección que declaré en mi solicitud, 5301 Northwest 36th Street, en Miami.'),
]

INTERMEDIAS = [
    ('¿Quién paga su viaje?', ' El DS-160 lo dejó en blanco. Si AME cubre el viaje, dilo sin dudar; si no, di quién lo paga y con qué.', 'Mi empleador, AME, cubre los gastos de mi viaje.'),
    ('¿Cuánto gana usted al mes?', '$2,418 mensuales, exactos como en el DS-160.', 'Dos mil cuatrocientos dieciocho dólares mensuales, como responsable de talento humano en AME.'),
    ('¿Desde cuándo trabaja en AME y dónde trabajaba antes?', 'Antes: Coordinación Zonal 4 de Salud, 2005 al 1 de febrero de 2026..', 'Trabajé 21 años en la Coordinación Zonal 4 de Salud, en Manabí, como analista de planificación, y desde 2026 estoy en AME como responsable de talento humano.'),
    ('¿Es la primera vez que va a Estados Unidos? ¿Le han negado alguna visa?', 'Primer viaje, nunca ha tenido visa, sin rechazos.', 'Sí, es la primera vez que solicito visa y que viajaría a Estados Unidos. No me han negado ninguna visa.'),
    ('¿Ha viajado antes fuera de Ecuador?', 'El DS-160 dice que no ha viajado en 5 años. Respuesta tal cual, sin inventar.', 'En los últimos cinco años no he viajado fuera de Ecuador. Este es mi primer viaje internacional reciente.'),
    ('¿Qué estudió usted?', 'Tres estudios: ingeniería, diplomado y maestría (los dos últimos virtuales). Dilos tal cual, en orden..', 'Soy ingeniera en Administración Pública por la Universidad Luis Vargas Torres, de Esmeraldas. También hice un diplomado en Gestión Pública y una maestría en Alta Dirección, ambos en línea.'),
    ('Vive en Portoviejo y trabaja en Quito. ¿Cómo lo organiza?', 'Eres soltera.. Responde con tu realidad exacta.', 'Soy soltera. Mi domicilio y mi familia están en Portoviejo, y trabajo en AME en Quito.'),
]

DIFICILES = [
    ('Usted tiene dos hijos con residencia permanente en Estados Unidos. ¿Por qué no ha pedido vivir allá con ellos?', 'LA pregunta clave. Respuesta tranquila y verdadera: tu vida y tu trabajo están en Ecuador. No te pongas a la defensiva..', 'Mis hijos viven allá, es cierto, y los quiero mucho. Pero mi vida, mi trabajo y mi familia están en Ecuador. Este viaje es por un workshop de alto nivel, por tres noches, y regreso a mi trabajo.'),
    ('Su solicitud dice que estudió una maestría en Boston y nunca ha estado en Estados Unidos. ¿Cómo es posible?', 'CLAVE: la maestría fue virtual. Dilo claro y sin dudar.', 'Fue una maestría virtual, en línea. Nunca he viajado a Estados Unidos; esta sería mi primera vez.'),
    ('¿Quién es Jaime Narváez y qué relación tiene con usted?', 'Es tu contacto en EE.UU. según el DS-160 (socio de negocios, Comité Int Cumbre de New York)..', 'El señor Jaime Narváez es el Presidente Ejecutivo del comité que organiza el workshop y firmó mi carta de invitación. Lo conozco por el trabajo.'),
    ('¿Qué va a hacer usted, que trabaja en talento humano, en ese evento en Miami?', 'Explica el valor para tu cargo: gestión pública y de personal, redes de contactos..', 'Mi trabajo es la gestión del personal de una institución pública. En el workshop sobre comunicación y manejo de crisis para gobiernos municipales y regionales voy a conocer experiencias de gestión pública y a traer lo aprendido para AME.'),
    ('¿Qué garantía tengo de que usted regresará a Ecuador?', 'Tu arraigo: trabajo en AME, familia, padres en Ecuador, viaje corto.', 'Mi trabajo en AME me espera, mi familia y mis padres están en Ecuador, y el viaje dura tres noches con regreso el 6 de diciembre.'),
    ('¿Cuánto tiempo hace que sus hijos viven en Estados Unidos y los visitará durante el viaje?', 'No ocultes el vínculo con tus hijos; responde con la verdad exacta..', 'Mis hijos viven allá desde hace algún tiempo. Mi viaje es por el workshop de alto nivel, mi hospedaje ya está definido y regreso a Ecuador el 6 de diciembre.'),
]

TRAMPA = [
    ('¿Ha sufrido daños, violencia o maltrato en su país de origen o en su última residencia habitual?', 'CRÍTICA — pregunta obligatoria 2026 para detectar posibles solicitantes de asilo. Un «sí» puede derivar en negativa automática. Responde con seguridad.', 'No, nunca he sufrido daños, violencia ni maltrato en Ecuador. Vivo y trabajo con normalidad en mi país.'),
    ('¿Teme sufrir daños, persecución o maltrato si regresa a ese país?', 'CRÍTICA — segunda pregunta obligatoria 2026. No tienes motivo real para temer volver.', 'No, no tengo ningún temor de regresar a Ecuador. Es mi país, donde vivo y trabajo.'),
    ('Sus hijos son residentes en EE.UU. Cuando ellos sean ciudadanos, ¿lo pedirán a usted?', 'No te cierres ni inventes: respuesta tranquila, sin ofrecer más.', 'No lo sé ni lo he planeado. Mi vida está en Ecuador, y hoy solo viajo tres noches a un workshop de alto nivel.'),
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
        "<b>Jaime Narváez</b>, del Comité Int Cumbre de New York. Tu hospedaje: <b>5301 Northwest 36th Street (dirección del DS-160)</b>. "
        "Es tu primer viaje a Estados Unidos, sin rechazos previos. Trabajas en AME, en la administración de personal, tras 21 años en el sector público. "
        "<b>Tu entrevista es el miércoles 18 de noviembre de 2026, 8:00 AM.</b>", style_body))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("FORTALEZAS DE TU CASO", style_eyebrow))
    story.append(strength_box('', '21 años de trayectoria continua en el sector público', 'Del 2005 al 2026 en la Coordinación Zonal 4 de Salud y hoy en AME: carrera estable en gestión de talento humano.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Cargo actual de responsabilidad en AME', 'Responsable de la administración de personal de la institución, con salario declarado de $2,418 mensuales.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Formación acorde a tu cargo', 'Ingeniería en Administración Pública, diplomado en Gestión Pública y maestría en Alta Dirección (estos dos virtuales): todo coherente con tu trabajo.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Viaje corto y con propósito claro', 'Tres noches en Miami (3 al 6 de diciembre) para un workshop de alto nivel, con contacto en EE.UU. verificable.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Arraigo en Ecuador', 'Vive en Portoviejo, trabaja en AME y sus padres viven en Ecuador. Sin rechazos previos.'))
    story.append(Spacer(1, 2 * mm))
    story.append(Spacer(1, 3 * mm))
    story.append(CondPageBreak(75 * mm))
    story.append(Paragraph("PUNTOS A PREPARAR CON CALMA", style_eyebrow))
    story.append(risk_box('', 'Dos hijos residentes permanentes en EE.UU.', 'Es el punto más sensible: el oficial va a preguntar si ellos la pueden pedir. Responde con calma y la verdad: viajas por el evento, no a quedarte, y tu vida y tu trabajo están en Ecuador..'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Maestría y diplomado virtuales (Boston y México)', 'Tu DS-160 dice que nunca has estado en EE.UU. ni has viajado en 5 años, y a la vez registra una maestría en Boston (2022-2024) y un diplomado en México (2022). Ambos fueron virtuales: dilo con naturalidad y sin dudar, y recuerda que nunca has viajado.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Primera vez en EE.UU. y sin viajes en 5 años', 'No tienes historial de viajes que respalde tu retorno. Se compensa con tu trabajo, tu familia y un viaje corto con motivo de negocios.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Quién paga y qué evento es', 'El DS-160 dejó en blanco quién paga el viaje, y el contacto es el «Comité Int Cumbre de New York» en un hotel de Miami. Ten claro quién te invita, quién paga y qué vas a hacer cada día..'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Empleo reciente en AME', 'Llevas pocos meses en AME (antes 21 años en Salud). Prepara la explicación: cómo y cuándo pasaste de una institución a otra, y por qué AME te envía a este evento.'))
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
    bloque_preguntas(story, "NIVEL DIFICIL", "Aquí se decide la entrevista — el punto clave: tus dos hijos residentes en EE.UU.",
                     DIFICILES, RED, colors.HexColor("#FFF1F2"))
    story.append(CondPageBreak(90 * mm))

    story.append(Paragraph("MODO OFICIAL CONSULAR", style_eyebrow))
    story.append(Paragraph("Preguntas trampa — practica sin ver la respuesta primero", style_h2))
    story.append(Paragraph("Incluye las 2 preguntas obligatorias 2026 sobre asilo y las de tus hijos. Responde con calma, sin contradecirte, en 2 o 3 frases.", style_body))
    bloque_preguntas(story, "PREGUNTAS TRAMPA", "El oficial busca inconsistencias — mantén la calma", TRAMPA, RED, REDBG, es_trampa=True)
    story.append(PageBreak())

    story.append(Paragraph("CHECKLIST DE DOCUMENTOS", style_eyebrow))
    story.append(Paragraph("Lo que debes llevar a tu entrevista", style_h2))
    story.append(Spacer(1, 2 * mm))
    story.append(grupo_header("DOCUMENTOS OBLIGATORIOS", "Sin estos no puedes presentarte a la cita", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    obligatorios = [
        ("1", "Pasaporte vigente", f"Número {PASAPORTE}, vence 27 de enero de 2035."),
        ("2", "Confirmación DS-160", f"Código de barras legible, número {DS160}."),
        ("3", "Página de confirmación e instrucciones de la cita", "Impresa desde ais.usvisa-info.com, con el código de barras de tu cita (miércoles 18 de noviembre de 2026, 8:00 AM)."),
        ("4", "Fotografía 5x5 cm a color", "Tomada dentro de los últimos 6 meses, fondo claro."),
        ("5", "Comprobante de pago de la tasa MRV", "Guárdalo impreso — puede ser solicitado en la entrevista."),
        ("6", "Cédula de identidad", "Original y copia, como respaldo adicional de identidad."),
    ]
    for num, titulo, desc in obligatorios:
        story.append(doc_item(num, titulo, desc, GOLD2))
    story.append(Spacer(1, 5 * mm))
    story.append(grupo_header("DOCUMENTOS DE TRABAJO E INGRESOS", "Respaldan tu cargo en AME y tu ingreso mensual", BLUE, BLUEBG))
    story.append(Spacer(1, 2 * mm))
    laborales = [
        ("7", "Certificado laboral de AME", "Cargo, fecha de ingreso, salario y la autorización de tu viaje al evento."),
        ("8", "Rol de pagos de AME", "Los últimos 3 meses: respalda el salario de $2,418 declarado en el DS-160."),
        ("9", "Certificado de la Coordinación Zonal 4 de Salud", "Respalda tus 21 años de trayectoria (2005 a febrero de 2026) y la salida de ese cargo."),
        ("10", "Estados de cuenta bancarios de 6 meses", "Muestran movimiento coherente con tus ingresos."),
        ("11", "Carta de quien cubre los gastos del viaje", "Si paga AME, debe decir que AME paga el viaje y que regresas a tu cargo (el DS-160 dejó en blanco quién paga)."),
        ("12", "Títulos y certificados de tus estudios", "Ingeniería en Administración Pública, diplomado en Gestión Pública y maestría en Alta Dirección; el diplomado y la maestría fueron virtuales."),
    ]
    for num, titulo, desc in laborales:
        story.append(doc_item(num, titulo, desc, BLUE))
    story.append(Spacer(1, 5 * mm))
    story.append(grupo_header("VIAJE Y RESPALDO ADICIONAL", "Completan tu expediente para la entrevista", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    adicional = [
        ("13", "Carta de invitación al workshop de Miami", "Carta del Comité Internacional de la Cumbre Latinoamericana de New York (30 de octubre de 2026), firmada por Jaime Narváez, Presidente Ejecutivo: workshop del 4 de diciembre en el Hotel Indigo Miami Brickell. Llévala impresa, con el comprobante de la inscripción ($500 por persona) si ya la pagaste."),
        ("14", "Reserva de hospedaje", "Dirección del DS-160: 5301 Northwest 36th Street — del 3 al 6 de diciembre."),
        ("15", "Itinerario de vuelo (ida y vuelta)", "Con regreso fijo a Ecuador el 6 de diciembre."),
        ("16", "Seguro de viaje / asistencia médica internacional", "Cobertura para todo el periodo del viaje."),
        ("17", "Documentos de arraigo familiar", "Partidas de nacimiento de tus hijos y cédula de tus padres: solo por si el oficial lo pide."),
    ]
    for num, titulo, desc in adicional:
        story.append(doc_item(num, titulo, desc, GOLD2))
    story.append(PageBreak())

    story.append(Paragraph("ULTIMO PASO", style_eyebrow))
    story.append(Paragraph("El día de tu cita", style_h2))
    story.append(Paragraph(
        "Tu cita es el <b>miércoles 18 de noviembre de 2026, 8:00 AM</b> en la Embajada de EE.UU. en Quito (Av. Avigiras E12-170 y Guayacanes, frente al Hospital SOLCA). "
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
    story.append(strength_box("", "Dentro de la entrevista", "Responde solo lo que te preguntan, habla claro y sin apresurarte. Si preguntan por tus hijos, responde con calma y con la verdad: viajas por el evento, tu vida y tu trabajo están en Ecuador, y regresas el 6 de diciembre."))
    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="100%", color=LINE, thickness=1))
    story.append(Spacer(1, 6 * mm))
    story.append(closing_band())
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF generado: {OUT_PATH}")


if __name__ == "__main__":
    build()
