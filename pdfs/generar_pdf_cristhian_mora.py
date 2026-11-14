"""
Genera pdf-cristhian-mora.pdf -- Guia personalizada + checklist + preguntas
Visa B1/B2 USA -- Jorge Cristhian Mora Larrea
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

CLIENTE = "Cristhian Mora"
CLIENTE_COMPLETO = "Jorge Cristhian Mora Larrea"
DESTINO = "Miami, EE.UU."
FECHA_CITA = "30 nov 2026, 08:00"
LUGAR_CITA = "Embajada de EE.UU. en Quito"
DS160 = "AA00FWR8L1"
PASAPORTE = "B1579196"

OUT_PATH = os.path.join(os.path.dirname(__file__), "pdf-cristhian-mora.pdf")

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
        f"<font size=9 color='#475569'>{PASAPORTE} · vence 7 ago 2036</font>",
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
        "<font color='#FFFFFF' size=13><b>Gracias por confiar tu proceso en nosotros, Cristhian.</b></font><br/>"
        "<font color='#94A3B8' size=9>Tu cita: lunes 30 de noviembre, 8:00 AM — practica cada día y escríbenos por WhatsApp ante cualquier duda.</font>",
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
    ('¿Cuál es el propósito de su viaje a Estados Unidos?', 'Workshop de alto nivel (negocios) en Miami. Respuesta directa y corta.', 'Viajo por negocios a Miami, Florida, tres noches, del 3 al 6 de diciembre, a un workshop de alto nivel sobre comunicación y manejo de crisis para gobiernos municipales y regionales, organizado por el Comité Internacional de la Cumbre Latinoamericana de New York.'),
    ('¿A qué se dedica usted?', 'Tu cargo real: eres el Viceministro de Gobierno del Ecuador. Dilo directo.', 'Soy el Viceministro de Gobierno del Ecuador. Coordino y superviso a las gobernaciones e intendencias del país para garantizar el orden público y el control territorial.'),
    ('¿Cuánto tiempo se va a quedar?', 'Tres noches: del 3 al 6 de diciembre.', 'Tres noches. Llego el 3 de diciembre y regreso a Ecuador el 6 de diciembre.'),
    ('¿Dónde se va a hospedar?', 'Dirección del DS-160: 145 SW 11th Street, Hotel Indigo Miami Brickell, Miami. Ten tu reserva a mano.', 'En el Hotel Indigo Miami Brickell, en 145 SW 11th Street, en Miami. Tengo mi reserva para las tres noches.'),
]

INTERMEDIAS = [
    ('¿Le han negado alguna visa? ¿Es la primera vez que va a Estados Unidos?', 'CRÍTICA — Sí: en 1999 te negaron una visa (214b). Dilo sin dudar y sin adornos. Primera vez en EE.UU.', 'Sí. En 1999, a los 20 años, me negaron una visa por la sección 214(b). Desde entonces he tenido una carrera estable en Ecuador, sin ningún otro problema migratorio. Esta es la primera vez que viajaría a Estados Unidos.'),
    ('¿Quién paga su viaje?', 'Paga tu empleador, el Viceministerio de Gobierno (el DS-160 no lo muestra). Dilo sin dudar y ten la carta a mano.', 'Mi empleador, el Viceministerio de Gobierno, cubre los gastos de mi viaje. Tengo la carta que lo respalda.'),
    ('¿Cuánto gana usted al mes?', '$4,283 mensuales, exactos como en el DS-160.', 'Cuatro mil doscientos ochenta y tres dólares mensuales, como Viceministro de Gobierno.'),
    ('¿Desde cuándo trabaja ahí y dónde trabajaba antes?', 'Antes: Asamblea Nacional (ago 2021 – may 2025) y AME (may 2019 – jul 2021). La fecha en que asumiste como Viceministro no consta en el DS-160: tenla clara.', 'Fui Asesor Legislativo en la Asamblea Nacional hasta mayo de 2025, y antes asesor de gestión jurídico y político en AME. Hoy soy el Viceministro de Gobierno desde [fecha en que asumiste].'),
    ('¿Ha viajado antes fuera de Ecuador?', 'Sí: Colombia y Perú. Cítalos tal cual están en el DS-160.', 'Sí. En los últimos cinco años viajé a Colombia y a Perú, y siempre regresé a Ecuador.'),
    ('¿Qué estudió usted?', 'Tres estudios. Dilos en orden y aclara la modalidad de la maestría.', 'Estudié Derecho en la UTPL, soy tecnólogo en Política y Gobierno por ILADES, y tengo una maestría en Comunicación Política Avanzada de la Universidad de Lleida.'),
    ('¿Está casado? ¿Su familia viaja con usted?', 'Casado con Johanna Peralta. Viajas solo. El DS-160 no menciona hijos.', 'Sí, estoy casado con Johanna. Viajo solo y regreso el 6 de diciembre; mi esposa, mi hogar y mi trabajo están en Quito.'),
]

DIFICILES = [
    ('Hace 27 años le negaron una visa. ¿Qué ha cambiado desde entonces?', 'Tu pregunta más probable. Breve, tranquila, sin discutir la negativa.', 'Tenía 20 años y no tenía mi vida formada. Hoy tengo 47, una carrera estable de 27 años en Ecuador, soy el Viceministro de Gobierno, y mi esposa y mi hogar están en Quito. Viajo tres noches y regreso.'),
    ('¿Qué garantía tengo de que usted regresará a Ecuador?', 'Tu arraigo: trabajo, esposa, hogar en Quito, padres en Ecuador, viaje corto.', 'Mi cargo de Viceministro me espera, mi esposa, mi casa y mis padres están en Ecuador, y el viaje dura tres noches con regreso el 6 de diciembre.'),
    ('¿Qué va a hacer exactamente en ese workshop en Miami y qué relación tiene con su cargo?', 'El workshop (4 de diciembre, Hotel Indigo Miami Brickell) trata de comunicación y manejo de crisis para gobiernos municipales y regionales: conéctalo con tu trabajo con gobernaciones e intendencias. Lleva la carta de invitación.', 'Voy al workshop de alto nivel «Comunicación y manejo de crisis para Gobiernos Municipales y regionales», el 4 de diciembre en Miami. Es un tema de mi trabajo con gobernaciones e intendencias; regreso el 6 de diciembre a aplicar lo aprendido.'),
    ('¿Quién es Jaime Narváez y qué relación tiene con usted?', 'Es el Presidente Ejecutivo del Comité Internacional de la Cumbre Latinoamericana de New York y firma tu carta de invitación. Ten claro cómo lo conoces.', 'El señor Jaime Narváez es el Presidente Ejecutivo del comité que organiza el workshop y firmó mi carta de invitación. Lo conozco por [cómo lo conoces].'),
    ('Su maestría es de la Universidad de Lleida, en España. ¿Viajó para estudiarla?', 'Fue virtual, por eso el DS-160 no registra viaje a España. Dilo claro y sin dudar.', 'No viajé a España. Fue un programa virtual; lo cursé desde Ecuador mientras trabajaba en la Asamblea Nacional.'),
    ('Usted es el Viceministro de Gobierno y su institución paga el viaje. ¿Por qué un workshop de alto nivel en Miami?', 'Tu pregunta más delicada por el cargo. Ten claro el beneficio del workshop (comunicación y manejo de crisis para gobiernos municipales y regionales) y que viajas con visa de visitante, no en misión oficial.', 'Voy por negocios al workshop «Comunicación y manejo de crisis para Gobiernos Municipales y regionales», un tema de mi trabajo con gobernaciones e intendencias. El Viceministerio cubre mis gastos y regreso a mi cargo el 6 de diciembre.'),
]

TRAMPA = [
    ('¿Ha sufrido daños, violencia o maltrato en su país de origen o en su última residencia habitual?', 'CRÍTICA — pregunta obligatoria 2026 para detectar posibles solicitantes de asilo. Un «sí» puede derivar en negativa automática. Responde con seguridad.', 'No, nunca he sufrido daños, violencia ni maltrato en Ecuador. Vivo y trabajo con normalidad en mi país.'),
    ('¿Teme sufrir daños, persecución o maltrato si regresa a ese país?', 'CRÍTICA — segunda pregunta obligatoria 2026. No tienes motivo real para temer volver.', 'No, no tengo ningún temor de regresar a Ecuador. Es mi país, donde vivo y trabajo.'),
    ('Usted es funcionario del gobierno. ¿Viaja en misión oficial?', 'Aplicas con visa B1/B2 (visitante), o sea un viaje no oficial. Dilo claro y corto.', 'No. Viajo por negocios a un workshop de alto nivel, de tres noches, con visa de visitante, y regreso a mi cargo en el Viceministerio el 6 de diciembre.'),
    ('¿Piensa trabajar o quedarse a vivir en Estados Unidos?', 'No lo contemples ni como hipótesis. Respuesta corta.', 'No. Voy tres noches al workshop y regreso a mi cargo y a mi hogar en Quito.'),
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
        "<b>Jaime Narváez</b>, Presidente Ejecutivo del Comité Internacional de la Cumbre Latinoamericana de New York (workshop del 4 de diciembre). Tu hospedaje: <b>145 SW 11th Street, Hotel Indigo Miami Brickell, Miami, Florida 33130 (dirección del DS-160)</b>. "
        "Es tu primer viaje a Estados Unidos; declaraste una negativa de 1999 y has tenido 27 años de carrera estable. Eres el Viceministro de Gobierno del Ecuador, tras haber sido Asesor Legislativo en la Asamblea Nacional, y el Viceministerio paga tu viaje. "
        "<b>Tu entrevista es el lunes 30 de noviembre de 2026, 8:00 AM.</b>", style_body))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("FORTALEZAS DE TU CASO", style_eyebrow))
    story.append(strength_box('', 'Carrera estable de 27 años', 'Declaraste que desde 1999 has tenido una carrera profesional estable en los sectores público y privado de Ecuador, sin ningún otro problema migratorio.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Viceministro de Gobierno del Ecuador', 'Un cargo de máxima responsabilidad: coordinas y supervisas las gobernaciones e intendencias del país, con un salario declarado de $4,283 mensuales.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Trayectoria coherente y verificable', 'Asesor Legislativo en la Asamblea Nacional (2021-2025) y Asesor de Gestión Jurídico y Político en AME (2019-2021), siempre en gestión pública.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Formación sólida', 'Derecho en la UTPL, Tecnología en Política y Gobierno (ILADES) y maestría en Comunicación Política Avanzada (Lleida), acordes a tu carrera.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Arraigo en Ecuador', 'Casado, con tu hogar en Quito, tus padres en Ecuador, sin familiares en EE.UU. y un viaje corto de tres noches. Viajaste a Colombia y Perú y regresaste.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Honestidad al declarar', 'Declaraste tu negativa de 1999 con claridad, y eso suma credibilidad: lo importante es explicar con calma qué cambió desde entonces.'))
    story.append(Spacer(1, 2 * mm))
    story.append(Spacer(1, 3 * mm))
    story.append(CondPageBreak(75 * mm))
    story.append(Paragraph("PUNTOS A PREPARAR CON CALMA", style_eyebrow))
    story.append(risk_box('', 'Negativa 214(b) en 1999', 'Es el punto más importante: el oficial lo verá en tu DS-160 y preguntará qué cambió. Responde breve y con calma: fue hace 27 años, a los 20 años, y desde entonces tu vida y tu trabajo están en Ecuador.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Primera vez en EE.UU. con viaje a un workshop', 'Nunca has estado en EE.UU. y solo viajaste a Colombia y Perú. Lo que más pesa es que el motivo sea claro: qué workshop es, quién te invita y qué vas a hacer cada día.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Eres funcionario de alto nivel y el Viceministerio paga el viaje', 'Siendo el Viceministro de Gobierno, el oficial querrá saber por qué viajas a un workshop de alto nivel y por qué lo paga el Viceministerio. Ten clara una explicación breve y verdadera, la carta del Viceministerio y el programa del evento. Aplicas con visa B1/B2, un viaje no oficial.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Maestría en línea en España', 'Tu maestría de la Universidad de Lleida (España) fue virtual: dilo con naturalidad. Por eso tu DS-160 no registra ningún viaje a España.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Primer viaje y pocos viajes previos', 'Solo viajaste a Colombia y Perú. Se compensa con tu cargo, tu esposa y tu hogar en Quito, tus padres en Ecuador y un viaje corto de tres noches.'))
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
    bloque_preguntas(story, "NIVEL DIFICIL", "Aquí se decide la entrevista — el punto clave: tu negativa de 1999 y tu cargo de Viceministro",
                     DIFICILES, RED, colors.HexColor("#FFF1F2"))
    story.append(CondPageBreak(90 * mm))

    story.append(Paragraph("MODO OFICIAL CONSULAR", style_eyebrow))
    story.append(Paragraph("Preguntas trampa — practica sin ver la respuesta primero", style_h2))
    story.append(Paragraph("Incluye las 2 preguntas obligatorias 2026 sobre asilo y las de tu negativa de 1999 y tu cargo de Viceministro de Gobierno. Responde con calma, sin contradecirte, en 2 o 3 frases.", style_body))
    bloque_preguntas(story, "PREGUNTAS TRAMPA", "El oficial busca inconsistencias — mantén la calma", TRAMPA, RED, REDBG, es_trampa=True)
    story.append(PageBreak())

    story.append(Paragraph("CHECKLIST DE DOCUMENTOS", style_eyebrow))
    story.append(Paragraph("Lo que debes llevar a tu entrevista", style_h2))
    story.append(Spacer(1, 2 * mm))
    story.append(grupo_header("DOCUMENTOS OBLIGATORIOS", "Sin estos no puedes presentarte a la cita", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    obligatorios = [
        ("1", "Pasaporte vigente", f"Número {PASAPORTE}, vence 7 de agosto de 2036."),
        ("2", "Confirmación DS-160", f"Código de barras legible, número {DS160}."),
        ("3", "Página de confirmación e instrucciones de la cita", "Impresa desde ais.usvisa-info.com, con el código de barras de tu cita (lunes 30 de noviembre de 2026, 8:00 AM)."),
        ("4", "Fotografía 5x5 cm a color", "Tomada dentro de los últimos 6 meses, fondo claro."),
        ("5", "Comprobante de pago de la tasa MRV", "Guárdalo impreso — puede ser solicitado en la entrevista."),
        ("6", "Cédula de identidad", "Original y copia, como respaldo adicional de identidad."),
    ]
    for num, titulo, desc in obligatorios:
        story.append(doc_item(num, titulo, desc, GOLD2))
    story.append(Spacer(1, 5 * mm))
    story.append(grupo_header("DOCUMENTOS DE TRABAJO E INGRESOS", "Respaldan tu cargo y tu trayectoria", BLUE, BLUEBG))
    story.append(Spacer(1, 2 * mm))
    laborales = [
        ("7", "Certificado laboral del Viceministerio de Gobierno", "Cargo de Viceministro, fecha de ingreso, salario de $4,283 y la autorización de tu viaje al evento."),
        ("8", "Rol de pagos de los últimos 3 meses", "Respalda el salario de $4,283 declarado en el DS-160."),
        ("9", "Certificados de la Asamblea Nacional y de AME", "Respaldan tus cargos como Asesor Legislativo (2021-2025) y Asesor de Gestión Jurídico y Político (2019-2021)."),
        ("10", "Estados de cuenta bancarios de 6 meses", "Muestran movimiento coherente con tus ingresos."),
        ("11", "Carta del Viceministerio de Gobierno", "Carta que diga que el Viceministerio cubre los gastos de tu viaje y que regresas a tu cargo (el DS-160 dejó en blanco quién paga)."),
        ("12", "Títulos y certificados de tus estudios", "Derecho (UTPL), tecnología en Política y Gobierno (ILADES) y maestría de la Universidad de Lleida (virtual)."),
    ]
    for num, titulo, desc in laborales:
        story.append(doc_item(num, titulo, desc, BLUE))
    story.append(Spacer(1, 5 * mm))
    story.append(grupo_header("VIAJE Y RESPALDO ADICIONAL", "Completan tu expediente para la entrevista", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    adicional = [
        ("13", "Carta de invitación al workshop de Miami", "Carta del Comité Internacional de la Cumbre Latinoamericana de New York (11 de noviembre de 2026), firmada por Jaime Narváez, Presidente Ejecutivo: workshop del 4 de diciembre en el Hotel Indigo Miami Brickell. Llévala impresa."),
        ("14", "Reserva de hospedaje", "Hotel Indigo Miami Brickell, 145 SW 11th Street (dirección del DS-160) — del 3 al 6 de diciembre."),
        ("15", "Itinerario de vuelo (ida y vuelta)", "Con regreso fijo a Ecuador el 6 de diciembre."),
        ("16", "Seguro de viaje / asistencia médica internacional", "Cobertura para todo el periodo del viaje."),
        ("17", "Documentos de arraigo familiar", "Certificado de matrimonio y cédulas de tu esposa y de tus padres: solo por si el oficial lo pide."),
    ]
    for num, titulo, desc in adicional:
        story.append(doc_item(num, titulo, desc, GOLD2))
    story.append(PageBreak())

    story.append(Paragraph("ULTIMO PASO", style_eyebrow))
    story.append(Paragraph("El día de tu cita", style_h2))
    story.append(Paragraph(
        "Tu cita es el <b>lunes 30 de noviembre de 2026, 8:00 AM</b> en la Embajada de EE.UU. en Quito (Av. Avigiras E12-170 y Guayacanes, frente al Hospital SOLCA). "
        "Lleva la confirmación del DS-160 con el código de barras que corresponde a tu cita y tu pasaporte.", style_body))
    story.append(Spacer(1, 3 * mm))
    story.append(strength_box("", "Llega 20-30 minutos antes", "No más de 15 minutos antes de tu hora exacta de ingreso — no hay necesidad de llegar mucho antes."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("", "Vestimenta formal", "Como para una reunión importante — comunica seriedad."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("", "Qué llevar", "Pasaporte original, confirmación DS-160 impresa, página de confirmación de cita, comprobante de pago MRV, foto y los documentos de respaldo de tu cargo, de tus estudios y del evento."))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box("", "Qué NO llevar", "Celular (no pasa seguridad), laptop, tablet, cables, comida o bebidas."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("", "Dentro de la entrevista", "Responde solo lo que te preguntan, habla claro y sin apresurarte. Si preguntan por tu negativa de 1999, responde con calma y con la verdad: fue a los 20 años, y desde entonces tu vida y tu trabajo están en Ecuador. Viajas por el evento y regresas el 6 de diciembre."))
    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="100%", color=LINE, thickness=1))
    story.append(Spacer(1, 6 * mm))
    story.append(closing_band())
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF generado: {OUT_PATH}")


if __name__ == "__main__":
    build()
