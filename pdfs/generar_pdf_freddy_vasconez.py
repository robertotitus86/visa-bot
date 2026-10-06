"""
Genera pdf-freddy-vasconez.pdf -- Guia personalizada + checklist + preguntas
Visa B1/B2 USA -- Freddy Wilfrido Vásconez Freire
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

CLIENTE = "Freddy Vásconez"
CLIENTE_COMPLETO = "Freddy Wilfrido Vásconez Freire"
DESTINO = "Miami, EE.UU."
FECHA_CITA = "9 nov 2026, 9:00 AM"
LUGAR_CITA = "Embajada de EE.UU. en Quito"
DS160 = "AA00FTWGBH"
PASAPORTE = "B1032986"

OUT_PATH = os.path.join(os.path.dirname(__file__), "pdf-freddy-vasconez.pdf")

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
        f"<font size=9 color='#475569'>{PASAPORTE} · vence 3 oct 2035</font>",
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
        "<font color='#FFFFFF' size=13><b>Gracias por confiar tu proceso en nosotros, Freddy.</b></font><br/>"
        "<font color='#94A3B8' size=9>Tu cita es el 9 de noviembre — practica cada día y escríbenos por WhatsApp ante cualquier duda.</font>",
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
    ('¿Cuál es el propósito de su viaje a Estados Unidos?', 'Viaje de turismo, corto, a Miami. Respuesta directa.', 'Viajo a Miami de turismo, por seis días, a partir del 10 de febrero de 2027.'),
    ('¿A qué se dedica usted?', 'Su trabajo real: calzado y artículos de cuero, en Ibarra.', 'Me dedico a la confección, elaboración y reparación de calzado y de artículos de cuero, en Ibarra.'),
    ('¿Cuánto tiempo se va a quedar?', 'Seis días desde el 10 de febrero de 2027.', 'Seis días. Llego a Miami el 10 de febrero de 2027 y regreso a Ecuador al terminar el viaje.'),
    ('¿Dónde se va a hospedar?', 'Days Inn by Wyndham Miami Airport, Miami Springs.', 'Me hospedo en el hotel Days Inn by Wyndham Miami Airport, en la 4767 Northwest 36th Street, en Miami Springs, Florida.'),
    ('¿Tiene familiares en los Estados Unidos?', 'Ninguno. Respuesta corta y directa.', 'No, no tengo ningún familiar en los Estados Unidos.'),
]

INTERMEDIAS = [
    ('¿Quién paga su viaje?', 'DS-160: «SELF». Responda sin dudar.', 'Yo mismo, con los ingresos de mi trabajo.'),
    ('¿Cuánto gana usted al mes?', '$3,000 mensuales, exactos como en el DS-160.', 'Tres mil dólares mensuales, de mi trabajo en calzado y artículos de cuero.'),
    ('¿Es la primera vez que va a Estados Unidos? ¿Le han negado alguna visa?', 'Primer viaje, nunca ha tenido visa y no tiene rechazos.', 'Sí, es la primera vez que solicito visa y que viajaría a Estados Unidos. No me han negado ninguna visa.'),
    ('¿Ha viajado antes fuera de Ecuador?', 'Solo Colombia en los últimos cinco años. Dígalo tal cual.', 'Sí, he viajado a Colombia, y regresé a Ecuador sin ningún inconveniente.'),
    ('¿Es casado? ¿Con quién vive?', 'Divorciado desde 2011, por mutuo acuerdo. Sin dar de más.', 'Soy divorciado desde marzo de 2011, por mutuo acuerdo. Vivo y trabajo en Ibarra.'),
    ('¿Qué estudió?', 'Administración Aduanera, Liceo Aduanero, Ibarra, 2011-2013.', 'Estudié Administración Aduanera en el Instituto Tecnológico Superior Liceo Aduanero, en Ibarra, entre 2011 y 2013.'),
    ('¿Por qué eligió un hotel junto al aeropuerto y no uno en la zona turística?', 'No se ponga a la defensiva. Explique el motivo REAL (precio, cercanía, recomendación). Esta es una base honesta.', 'Lo escogí por el precio y por la facilidad de llegar desde el aeropuerto. Desde ahí me muevo a los lugares turísticos.'),
]

DIFICILES = [
    ('En su solicitud dice que es artista, pero usted hace calzado. ¿Cuál es su verdadera ocupación?', 'LA pregunta clave de su caso. Una sola explicación, clara y verdadera; igual las dos veces que se la hagan.', 'Mi oficio es la confección y reparación de calzado y artículos de cuero. Es un trabajo artesanal y en el formulario marqué la categoría que me pareció más cercana; mi actividad real es el calzado.'),
    ('¿Por qué quiere viajar a Miami?', 'Dígalo con sus propias palabras: lo importante es que sea su motivo REAL. Esta es una base.', 'Quiero conocer Miami por turismo. Es la primera vez que viajo a Estados Unidos y lo hago por seis días, pagando yo mismo mi viaje.'),
    ('No tiene itinerario ni conoce a nadie en Miami. ¿Qué va a hacer seis días allá?', 'El DS-160 dice «sin planes específicos». Tenga dos o tres actividades turísticas concretas para nombrar.', 'No conozco a nadie en Miami; solo tengo mi reserva de hotel. Voy a recorrer la ciudad como turista, conocer sus playas y sus lugares más conocidos, y regreso a Ecuador a mi trabajo.'),
    ('¿Qué garantía tengo de que usted regresará a Ecuador?', 'Su arraigo: vive y trabaja en Ibarra, viaje corto, autofinanciado.', 'Mi casa y mi trabajo están en Ibarra, donde vivo y trabajo en el mismo lugar. Es un viaje de solo seis días, lo pago yo mismo y regreso a mi trabajo.'),
    ('¿Cómo puedo comprobar que gana $3,000 al mes?', 'Es cuenta propia: respaldo con RUC, declaraciones del SRI y estados de cuenta. Llévelos.', 'Tengo mi RUC, mis declaraciones de impuestos y mis estados de cuenta, y se los puedo mostrar.'),
]

TRAMPA = [
    ('¿Ha sufrido daños, violencia o maltrato en su país de origen o en su última residencia habitual?', 'CRÍTICA — pregunta obligatoria 2026 para detectar posibles solicitantes de asilo. Un «sí» puede derivar en negativa automática. Responda con seguridad.', 'No, nunca he sufrido daños, violencia ni maltrato en Ecuador. Vivo y trabajo con normalidad en mi país.'),
    ('¿Teme sufrir daños, persecución o maltrato si regresa a ese país?', 'CRÍTICA — segunda pregunta obligatoria 2026. No tiene motivo real para temer volver.', 'No, no tengo ningún temor de regresar a Ecuador. Es mi país, donde vivo y trabajo.'),
    ('¿Por qué debería darle la visa a usted y no a cualquier otra persona?', 'La ley (Sección 214(b)) presume que todo solicitante quiere quedarse: demuéstrelo con hechos, sin sonar a súplica.', 'Porque mi vida y mi trabajo están en Ibarra, Ecuador. Es un viaje corto de turismo, lo pago yo mismo y no tengo ningún vínculo ni intención de quedarme en Estados Unidos.'),
    ('Usted tiene 61 años, es divorciado y casi no ha viajado. ¿Qué lo ata a Ecuador?', 'Responda con calma y con hechos: su trabajo, su casa, su vida en Ibarra. Si tiene hijos o padres que dependen de usted, menciónelos aquí.', 'Mi trabajo, mi casa y toda mi vida están en Ibarra. Este es un viaje corto de turismo y al terminar regreso a mi trabajo, como siempre.'),
    ('¿Piensa trabajar o quedarse a vivir en Estados Unidos?', 'No lo contemple ni como hipótesis. Respuesta corta.', 'No. Voy solo de turismo por seis días y regreso a mi trabajo en Ibarra.'),
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
    story.append(Paragraph("Motivo de viaje: turismo en Miami, 6 días", style_h2))
    story.append(Paragraph(
        "Viajas a <b>Miami</b> por turismo durante <b>seis días, desde el 10 de febrero de 2027</b>, solo y pagando tú mismo el viaje. "
        "Te hospedas en el <b>Days Inn by Wyndham Miami Airport, 4767 Northwest 36th Street, Miami Springs, Florida</b>. Es tu primer viaje a Estados Unidos, sin rechazos previos y sin familiares ni contactos allá. "
        "Vives y trabajas en Ibarra, donde confeccionas y reparas calzado y artículos de cuero.", style_body))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("FORTALEZAS DE TU CASO", style_eyebrow))
    story.append(strength_box('', 'Vive y trabaja en el mismo lugar, en Ibarra', 'Su domicilio y su lugar de trabajo coinciden (Rafael Larrea 3-59 y Simón Bolívar) — arraigo y estabilidad verificables.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Ingreso declarado de $3,000 mensuales, viaje autofinanciado', 'Paga él mismo el viaje: no depende de terceros ni de un patrocinador en EE.UU.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Antecedentes limpios y sin vínculos en EE.UU.', 'Sin rechazos, sin familiares ni contactos en Estados Unidos, pasaporte nuevo vigente hasta 2035.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Viaje corto y con reserva concreta', 'Seis días con hotel definido en Miami Springs — es una visita acotada, no una mudanza.'))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box('', 'Formación en Administración Aduanera', 'Estudió en el Instituto Tecnológico Superior Liceo Aduanero (Ibarra, 2011-2013): perfil formal y conocedor de trámites.'))
    story.append(Spacer(1, 2 * mm))
    story.append(Spacer(1, 3 * mm))
    story.append(CondPageBreak(75 * mm))
    story.append(Paragraph("PUNTOS A PREPARAR CON CALMA", style_eyebrow))
    story.append(risk_box('', 'Ocupación no coincide con el empleo en el DS-160', 'Figura como «Artista/Intérprete» pero su trabajo es confeccionar y reparar calzado. Debe explicarlo siempre igual, con la verdad, en una sola frase.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Poca historia de viajes', 'En 5 años solo declara Colombia y es su primer viaje a EE.UU. Se compensa con arraigo laboral y un viaje corto con motivo claro.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', 'Ingreso por cuenta propia: hay que respaldarlo', 'Lleve RUC, declaraciones del SRI y estados de cuenta que respalden los $3,000 mensuales.'))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box('', '«¿Por qué Miami?» y hotel junto al aeropuerto', 'No tiene itinerario detallado ni contacto en EE.UU. Prepare un motivo propio y real, en sus palabras, y mencione qué le gustaría hacer.'))
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
    bloque_preguntas(story, "NIVEL DIFICIL", "Aquí se decide la entrevista — el punto clave: por qué figuras como artista si haces calzado",
                     DIFICILES, RED, colors.HexColor("#FFF1F2"))
    story.append(CondPageBreak(90 * mm))

    story.append(Paragraph("MODO OFICIAL CONSULAR", style_eyebrow))
    story.append(Paragraph("Preguntas trampa — practica sin ver la respuesta primero", style_h2))
    story.append(Paragraph("Incluye las 2 preguntas obligatorias 2026 sobre asilo. Responde con calma, sin contradecirte, en 2 o 3 frases.", style_body))
    bloque_preguntas(story, "PREGUNTAS TRAMPA", "El oficial busca inconsistencias — mantén la calma", TRAMPA, RED, REDBG, es_trampa=True)
    story.append(PageBreak())

    story.append(Paragraph("CHECKLIST DE DOCUMENTOS", style_eyebrow))
    story.append(Paragraph("Lo que debes llevar a tu entrevista", style_h2))
    story.append(Spacer(1, 2 * mm))
    story.append(grupo_header("DOCUMENTOS OBLIGATORIOS", "Sin estos no puedes presentarte a la cita", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    obligatorios = [
        ("1", "Pasaporte vigente", f"Número {PASAPORTE}, vence 3 de octubre de 2035."),
        ("2", "Confirmación DS-160", f"Código de barras legible, número {DS160}."),
        ("3", "Página de confirmación e instrucciones de la cita", "Impresa desde ais.usvisa-info.com, con el código de barras de la cita del 9 de noviembre de 2026."),
        ("4", "Fotografía 5x5 cm a color", "Tomada dentro de los últimos 6 meses, fondo claro."),
        ("5", "Comprobante de pago de la tasa MRV", "Guárdelo impreso — puede ser solicitado en la entrevista."),
        ("6", "Cédula de identidad", "Original y copia, como respaldo adicional de identidad."),
    ]
    for num, titulo, desc in obligatorios:
        story.append(doc_item(num, titulo, desc, GOLD2))
    story.append(Spacer(1, 5 * mm))
    story.append(grupo_header("DOCUMENTOS DE TRABAJO E INGRESOS", "Respaldan tu actividad en Ibarra y tu ingreso mensual", BLUE, BLUEBG))
    story.append(Spacer(1, 2 * mm))
    laborales = [
        ("7", "RUC o RIMPE y patente municipal del negocio", "Demuestran que su taller de calzado existe formalmente en Ibarra (si los tiene)."),
        ("8", "Declaraciones del SRI de los últimos 12 meses", "Respaldan el ingreso de $3,000 mensuales declarado en el DS-160."),
        ("9", "Estados de cuenta bancarios de 6 meses", "Muestran movimiento coherente con sus ingresos y fondos para pagar el viaje."),
        ("10", "Fotos y facturas de su taller", "Del lugar de trabajo en Rafael Larrea y Simón Bolívar, Ibarra: evidencia de que su actividad es real."),
        ("11", "Título o certificado del Liceo Aduanero", "Administración Aduanera, 2011-2013: respalda su formación."),
    ]
    for num, titulo, desc in laborales:
        story.append(doc_item(num, titulo, desc, BLUE))
    story.append(Spacer(1, 5 * mm))
    story.append(grupo_header("VIAJE Y RESPALDO ADICIONAL", "Completan tu expediente para la entrevista", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    adicional = [
        ("12", "Reserva del hotel", "Days Inn by Wyndham Miami Airport, 4767 NW 36th Street, Miami Springs, Florida — desde el 10 de febrero de 2027, 6 días."),
        ("13", "Itinerario de vuelo (ida y vuelta)", "Con regreso fijo a Ecuador a los 6 días del viaje."),
        ("14", "Seguro de viaje / asistencia médica internacional", "Cobertura para todo el periodo del viaje."),
        ("15", "Sellos de viajes previos", "Colombia — evidencia de salida y regreso a Ecuador."),
        ("16", "Acta de divorcio", "Divorcio por mutuo acuerdo, 25 de marzo de 2011: solo por si el oficial lo pide."),
    ]
    for num, titulo, desc in adicional:
        story.append(doc_item(num, titulo, desc, GOLD2))
    story.append(PageBreak())

    story.append(Paragraph("ULTIMO PASO", style_eyebrow))
    story.append(Paragraph("El día de tu cita", style_h2))
    story.append(Paragraph(
        "Tu cita es el <b>lunes 9 de noviembre de 2026 a las 9:00 AM</b> en la Embajada de EE.UU. en Quito (Av. Avigiras E12-170 y Guayacanes, frente al Hospital SOLCA). "
        "Si necesitas reprogramar, puedes hacerlo hasta el 5 de noviembre de 2026, 5:00 AM, en tu página de resumen de solicitantes.", style_body))
    story.append(Spacer(1, 3 * mm))
    story.append(strength_box("", "Llega 20-30 minutos antes", "No más de 15 minutos antes de tu hora exacta de ingreso — no hay necesidad de llegar mucho antes."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("", "Vestimenta formal", "Como para una reunión importante — comunica seriedad."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("", "Qué llevar", "Pasaporte original, confirmación DS-160 impresa, página de confirmación de cita, comprobante de pago MRV, foto y documentos de respaldo de tu negocio."))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box("", "Qué NO llevar", "Celular (no pasa seguridad), laptop, tablet, cables, comida o bebidas."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("", "Dentro de la entrevista", "Responde solo lo que te preguntan, habla claro y sin apresurarte. Si preguntan por tu ocupación, explica una sola vez y con la verdad que tu oficio es el calzado y los artículos de cuero, y sigue adelante — sin justificarte de más."))
    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="100%", color=LINE, thickness=1))
    story.append(Spacer(1, 6 * mm))
    story.append(closing_band())
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF generado: {OUT_PATH}")


if __name__ == "__main__":
    build()
