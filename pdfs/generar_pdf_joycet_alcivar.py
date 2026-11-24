"""
Genera pdf-joycet-alcivar.pdf -- Guia personalizada + checklist + preguntas
Visa B1/B2 USA -- Joycet Alejandra Alcivar Alcivar
Cita: lunes 30 nov 2026, 8:30 AM, Consulado General de EE.UU. en Guayaquil
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

CLIENTE = "Joycet Alcivar"
CLIENTE_COMPLETO = "Joycet Alejandra Alcivar Alcivar"
DESTINO = "Orlando, EE.UU."
FECHA_CITA = "30 nov 2026, 08:30"
LUGAR_CITA = "Consulado General de EE.UU. en Guayaquil"
DS160 = "AA00FX9FL5"
PASAPORTE = "A8518412"
TOTAL_PAGES = 10

OUT_PATH = os.path.join(os.path.dirname(__file__), "pdf-joycet-alcivar.pdf")

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
    canvas.drawCentredString(cx, cy - 7 * mm, f"DE {TOTAL_PAGES}")

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
        f"<font size=9 color='#475569'>{PASAPORTE} · vence 3 ene 2033</font>",
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
        "<font color='#FFFFFF' size=13><b>Gracias por confiar tu proceso en nosotros, Joycet.</b></font><br/>"
        "<font color='#94A3B8' size=9>Tu cita: lunes 30 de noviembre, 8:30 AM — practica cada día y escríbenos por WhatsApp ante cualquier duda.</font>",
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
    ('¿Cuál es el propósito de su viaje a Estados Unidos?', 'Turismo en Orlando con tu mamá y tu familia. Respuesta directa y corta.', 'Voy de vacaciones a Orlando, Florida, cinco días, desde el 1 de marzo de 2027, con mi mamá y mi familia.'),
    ('¿Cuánto tiempo se va a quedar?', 'Cinco días desde el 1 de marzo de 2027. Ten clara la fecha exacta de regreso (el DS-160 solo dice 5 días).', 'Cinco días. Llego el 1 de marzo de 2027 y regreso a Ecuador al terminar esos cinco días.'),
    ('¿Dónde se va a hospedar?', 'Dirección del DS-160: The Point Hotel & Suites, 7389 Universal Boulevard, Orlando. Ten tu reserva a mano.', 'En The Point Hotel & Suites, en 7389 Universal Boulevard, en Orlando.'),
    ('¿Con quién viaja?', 'El DS-160 pone a 4 personas: tu mamá (Maira Alcivar), Armando Weir, Ashlyn y Clarissa Weir Alcivar. A tres los marcaste como «otro familiar»: ten clara la relación exacta con cada uno y explícala con naturalidad.', 'Viajo con mi mamá, Maira Alcivar; con Armando Weir, que es familiar mío; y con Ashlyn y Clarissa Weir Alcivar, también familiares.'),
]

INTERMEDIAS = [
    ('¿Quién paga su viaje?', 'Paga Armando Roberto Weir Casquete (en el DS-160: «otro familiar»). Dilo sin dudar y ten a mano su carta de respaldo y sus documentos.', 'Armando Weir, un familiar que viaja con nosotros, cubre los gastos del viaje. Tengo su carta de respaldo.'),
    ('¿A qué se dedica usted?', 'Trabajas como cajera en Corporación La Favorita y estudias Odontología. Dilo en ese orden y con tranquilidad.', 'Trabajo como cajera en Corporación La Favorita, en Plaza Vistana, en Daule, y estudio Odontología.'),
    ('¿Cuánto gana usted al mes?', '$800 mensuales, exactos como en el DS-160.', 'Ochocientos dólares mensuales, como cajera en La Favorita.'),
    ('¿Desde cuándo trabaja ahí y dónde trabajaba antes?', 'Antes: asistente de ventas en Ultra UV (2 oct 2023 – 11 mar 2025). La fecha de ingreso a La Favorita no consta en el DS-160: tenla clara, junto con qué hiciste entre ambos trabajos.', 'Trabajo en La Favorita desde [fecha de ingreso]. Antes fui asistente de ventas en Ultra UV, en Guayaquil, de octubre de 2023 a marzo de 2025.'),
    ('¿Qué estudia y dónde?', 'Odontología en la Universidad Bolivariana del Ecuador (Durán), desde octubre de 2024. El DS-160 pone fin de asistencia el 1 de noviembre de 2026: ten claro si sigues matriculada, qué ciclo cursas y cómo combinas estudio y trabajo.', 'Estudio Odontología en la Universidad Bolivariana del Ecuador, en Durán, desde octubre de 2024. Actualmente [ciclo / estado de matrícula].'),
    ('¿Ha viajado antes fuera de Ecuador?', 'Sí: República Dominicana, y es lo único que consta en el DS-160. Sé clara con cuándo fue y con quién. Es tu primera vez en EE.UU.', 'Sí, he viajado a República Dominicana y regresé a Ecuador. Esta sería mi primera vez en Estados Unidos.'),
    ('¿Dónde vive y tiene familiares en Estados Unidos?', 'Vives en Guayaquil (sector La Joya). El DS-160 dice que no tienes familiares en EE.UU. ni inmediatos ni otros.', 'Vivo en Guayaquil, en el sector La Joya. No tengo familiares en Estados Unidos; mi trabajo, mi carrera y mi familia están en Ecuador.'),
    ('¿Qué van a hacer en Orlando durante esos cinco días?', 'El DS-160 dice que no tienes planes específicos. Ten una idea concreta y verdadera de lo que harán (lugares, días). No inventes: cuenta solo lo que realmente tienen pensado.', 'Vamos de vacaciones a conocer Orlando: [lugares que tienen previstos]. Nos quedamos cinco días en el hotel y regresamos a Ecuador.'),
]

DIFICILES = [
    ('Hace más de tres años le negaron la visa. ¿Qué ha cambiado desde entonces?', 'Tu pregunta más probable. Breve, tranquila, sin discutir la negativa. Habla de lo que cambió: tu trabajo, tu carrera, tu vida en Ecuador.', 'Sí, en agosto de 2023 me negaron la visa porque no demostré suficientes lazos con mi país. Desde entonces he trabajado en Ultra UV y ahora en La Favorita, y estudio Odontología desde octubre de 2024. Mi vida y mi futuro están en Ecuador, y esta vez viajo cinco días de vacaciones con mi mamá.'),
    ('¿Qué garantía tengo de que usted regresará a Ecuador?', 'Tu arraigo: trabajo en La Favorita, carrera de Odontología, familia en Ecuador, viaje corto de cinco días.', 'Mi trabajo en La Favorita, mi carrera de Odontología y mi familia están en Ecuador, y el viaje dura solo cinco días. Tengo mi vida y mi futuro aquí.'),
    ('Su viaje lo paga Armando Weir. ¿Quién es él, a qué se dedica y por qué paga?', 'Es la pregunta más delicada: quien paga no es tu papá ni tu mamá. El DS-160 no trae su ocupación ni sus ingresos: ten claro quién es, a qué se dedica y por qué paga, y lleva su carta y sus documentos.', 'Armando Weir es familiar mío [relación exacta]. Él es [su ocupación] y cubre los gastos de la familia para estas vacaciones. Viaja con nosotros y tengo su carta de respaldo.'),
    ('¿Cuánto costará el viaje y cómo se financia?', 'Ten un estimado de vuelos, hotel y gastos, y qué parte cubre Armando. Con $800 al mes no cubrirías todo tú sola, y está bien: lo importante es que el respaldo de quien paga sea real y puedas explicarlo.', 'Calculamos aproximadamente [monto] entre vuelos, hotel y gastos. Armando lo cubre y tengo sus documentos de respaldo.'),
    ('Su mamá, Armando y su familia viajan con usted. ¿Quién se queda en Ecuador?', 'El oficial busca qué te ata a Ecuador cuando viaja la familia entera. Ten claro quién se queda (tu papá, otros familiares) y que tu trabajo y tu universidad te esperan.', 'Mi papá [y demás familiares] se quedan en Ecuador, y yo tengo mi trabajo en La Favorita y mi carrera esperándome. Es un viaje de vacaciones de cinco días.'),
    ('¿Cómo pidió permiso en su trabajo y en la universidad para viajar?', 'Ten claro si ya tienes vacaciones aprobadas en La Favorita para esas fechas y qué pasa con tus clases. Si aún no las pides, dilo con honestidad: las pedirás cuando tengas la visa.', 'En La Favorita [vacaciones aprobadas / las solicitaré con la visa] para esos días, y en la universidad [calendario / vacaciones]. Regreso a mi trabajo y a mis clases.'),
]

TRAMPA = [
    ('¿Ha sufrido daños, violencia o maltrato en su país de origen o en su última residencia habitual?', 'CRÍTICA — pregunta obligatoria 2026 para detectar posibles solicitantes de asilo. Un «sí» puede derivar en negativa automática. Responde con seguridad.', 'No, nunca he sufrido daños, violencia ni maltrato en Ecuador. Vivo, trabajo y estudio con normalidad en mi país.'),
    ('¿Teme sufrir daños, persecución o maltrato si regresa a ese país?', 'CRÍTICA — segunda pregunta obligatoria 2026. No tienes motivo real para temer volver.', 'No, no tengo ningún temor de regresar a Ecuador. Es mi país, donde vivo, trabajo y estudio.'),
    ('En su DS-160 su ocupación dice «Business». ¿A qué negocio se dedica?', 'En el formulario la ocupación principal quedó como «Business», pero tu empleo real es cajera y estudias Odontología. Aclara con naturalidad y sin inventar razones: no tienes negocio propio.', 'No tengo un negocio propio. Trabajo como cajera en La Favorita y estudio Odontología; esa casilla quedó así en el formulario, pero mi ocupación real es la que le acabo de decir.'),
    ('Dice que no tiene planes específicos, pero ya tiene fecha y hotel. ¿Ya tiene los tiquetes comprados?', 'Responde solo lo que es verdad. Lo más prudente es no comprar tiquetes sin tener la visa; si ya los compraste, dilo igual, sin dudar.', 'Tenemos la fecha tentativa de llegada, el 1 de marzo, y el hotel. Los tiquetes [aún no los compramos / ya están comprados].'),
    ('¿Tiene familiares, amigos o alguien esperándola en Estados Unidos?', 'No: el DS-160 dice que no tienes familiares en EE.UU. y que no conoces a nadie allá (contacto: el hotel). Respuesta corta.', 'No. No tengo familiares ni conocidos en Estados Unidos; solo conozco el hotel donde nos vamos a hospedar.'),
    ('¿Piensa trabajar o quedarse a vivir en Estados Unidos?', 'No lo contemples ni como hipótesis. Respuesta corta.', 'No. Voy cinco días de vacaciones y regreso a mi trabajo, a mi universidad y a mi casa en Guayaquil.'),
]

FORTALEZAS = [('Trabajo actual estable', 'Cajera en Corporación La Favorita, con un salario declarado de $800 mensuales, y experiencia previa como asistente de ventas en Ultra UV (oct 2023 – mar 2025).'), ('Estudiante de Odontología', 'Cursas Odontología en la Universidad Bolivariana del Ecuador desde octubre de 2024: una carrera en marcha que te ata a Ecuador.'), ('Viaje corto y en familia', 'Cinco días de vacaciones en Orlando, viajando con tu mamá y tu familia, con hospedaje definido en The Point Hotel & Suites.'), ('Sin familiares ni contactos en EE.UU.', 'No tienes familiares inmediatos ni otros familiares en Estados Unidos, ni peticiones de inmigrante a tu nombre.'), ('Honestidad al declarar', 'Declaraste con claridad tu negativa de 2023 (214b). Eso suma credibilidad: lo importante es explicar con calma qué cambió desde entonces.'), ('Pasaporte vigente y un viaje previo con retorno', 'Pasaporte vigente hasta 2033 y un viaje a República Dominicana en los últimos 5 años, del que regresaste a Ecuador.')]
RIESGOS = [('Negativa 214(b) de agosto de 2023', 'Es el punto más importante: el oficial la verá en tu DS-160 y preguntará qué cambió. Responde breve y con calma: tenías 19 años, y desde entonces trabajas, estudias Odontología y tu vida está en Ecuador.'), ('Quien paga no es tu papá ni tu mamá', 'Armando Weir figura como «otro familiar». Ten clara tu relación con él, a qué se dedica y por qué paga el viaje; lleva su carta de respaldo y sus documentos. El DS-160 no trae su ocupación ni sus ingresos.'), ('Primera vez en EE.UU. y poco historial de viaje', 'Solo viajaste a República Dominicana. Se compensa con tu trabajo, tu carrera, tu familia en Ecuador y un viaje corto de cinco días.'), ('Perfil joven, soltera y con ingreso modesto', 'Tienes 22 años y un salario de $800. Por eso pesa tanto que el patrocinador tenga respaldo real y que tu trabajo y tu carrera estén claros y comprobables.'), ('Ocupación «Business» y fechas en tu DS-160', 'El formulario marca tu ocupación principal como «Business» (tu empleo real es cajera) y no trae la fecha de ingreso a La Favorita; la carrera figura con fin de asistencia el 1 de nov de 2026. Ten claras estas tres cosas y respóndelas con naturalidad.')]
OBLIG = [('1', 'Pasaporte vigente', 'Número A8518412, vence el 3 de enero de 2033.'), ('2', 'Confirmación DS-160', 'Código de barras legible, número AA00FX9FL5. Es el que coincide con tu cita: NO lleves el anterior (AA00FW66SV).'), ('3', 'Página de confirmación e instrucciones de la cita', 'Impresa desde ais.usvisa-info.com, con el código de barras de tu cita (lunes 30 de noviembre de 2026, 8:30 AM, Guayaquil).'), ('4', 'Fotografía 5x5 cm a color', 'Tomada dentro de los últimos 6 meses, fondo claro.'), ('5', 'Comprobante de pago de la tasa MRV', 'Guárdalo impreso — puede ser solicitado en la entrevista.'), ('6', 'Cédula de identidad', 'Original y copia, como respaldo adicional de identidad.')]
LABORALES = [('7', 'Certificado laboral de Corporación La Favorita', 'Cargo de cajera, fecha de ingreso, salario de $800 y, si es posible, confirmación de tus vacaciones para el 1 de marzo de 2027.'), ('8', 'Rol de pagos de los últimos 3 meses', 'Respalda el salario de $800 declarado en el DS-160.'), ('9', 'Historial de aportes al IESS', 'Muestra la continuidad de tu vida laboral desde 2023.'), ('10', 'Certificado laboral de Ultra UV', 'Asistente de ventas, del 2 de octubre de 2023 al 11 de marzo de 2025.'), ('11', 'Certificado de matrícula y de estudios', 'Universidad Bolivariana del Ecuador, Odontología: debe mostrar que sigues matriculada, tu ciclo y tu calendario académico.'), ('12', 'Estados de cuenta bancarios de 6 meses', 'Muestran movimiento coherente con tus ingresos.')]
ADICIONAL = [('13', 'Carta de respaldo económico de Armando Weir', 'Que indique que cubre los gastos del viaje, con su cédula y comprobantes de su ocupación e ingresos (rol de pagos o RUC y estados de cuenta).'), ('14', 'Documentos de parentesco', 'Partida de nacimiento tuya y los documentos que muestren tu relación con tu mamá y con los familiares que viajan contigo.'), ('15', 'Reserva de hospedaje', 'The Point Hotel & Suites, 7389 Universal Boulevard, Orlando, Florida 32819 — desde el 1 de marzo de 2027 (5 días).'), ('16', 'Cotización o reserva de vuelo ida y vuelta', 'Con la fecha de regreso a Ecuador. Cuidado: no compres tiquetes hasta tener la visa.'), ('17', 'Seguro de viaje / asistencia médica internacional', 'Cobertura para todo el periodo del viaje.'), ('18', 'Copias de pasaportes y visas de quienes viajan contigo', 'Tu mamá, Armando, Ashlyn y Clarissa: si alguno ya tiene visa de EE.UU., lleva la copia.')]

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
    story.append(Paragraph(f"Hola {CLIENTE.split()[0]}, este es tu plan para llegar lista a tu entrevista", style_h2))
    story.append(Paragraph(
        "En <b>Asesoría Visa Global</b> preparamos contigo cada detalle de tu entrevista consular para la <b>visa B1/B2</b>. "
        "Este documento reúne tu guía de preguntas — incluidas las preguntas trampa del oficial consular — tus fortalezas, "
        "tu checklist de documentos y el protocolo del día de la cita, todo basado en tu DS-160 real. "
        "Donde veas [corchetes] en una respuesta modelo, completa con tu dato real.", style_body))
    story.append(Spacer(1, 3 * mm))
    story.append(cita_box())
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("TU CASO EN RESUMEN", style_eyebrow))
    story.append(Paragraph("Motivo de viaje: vacaciones en Orlando, 5 días, en familia", style_h2))
    story.append(Paragraph(
        "Viajas a <b>Orlando, Florida</b>, desde el <b>1 de marzo de 2027</b> por 5 días, con tu mamá y tu familia. Tu hospedaje: "
        "<b>The Point Hotel &amp; Suites, 7389 Universal Boulevard, Orlando, Florida 32819 (dirección del DS-160)</b>. "
        "Es tu primer viaje a Estados Unidos; declaraste una negativa de agosto de 2023 (214b). Trabajas como cajera en Corporación La Favorita, "
        "estudias Odontología y el viaje lo paga Armando Weir. "
        "<b>Tu entrevista es el lunes 30 de noviembre de 2026, 8:30 AM, en Guayaquil.</b>", style_body))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("FORTALEZAS DE TU CASO", style_eyebrow))
    for t, d in FORTALEZAS:
        story.append(strength_box('', t, d))
        story.append(Spacer(1, 2 * mm))
    story.append(Spacer(1, 3 * mm))
    story.append(CondPageBreak(75 * mm))
    story.append(Paragraph("PUNTOS A PREPARAR CON CALMA", style_eyebrow))
    for t, d in RIESGOS:
        story.append(risk_box('', t, d))
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
    bloque_preguntas(story, "NIVEL DIFICIL", "Aquí se decide la entrevista — el punto clave: tu negativa de 2023 y quién paga el viaje",
                     DIFICILES, RED, colors.HexColor("#FFF1F2"))
    story.append(CondPageBreak(90 * mm))

    story.append(Paragraph("MODO OFICIAL CONSULAR", style_eyebrow))
    story.append(Paragraph("Preguntas trampa — practica sin ver la respuesta primero", style_h2))
    story.append(Paragraph("Incluye las 2 preguntas obligatorias 2026 sobre asilo y las de tu ocupación, tus planes y tus contactos en EE.UU. Responde con calma, sin contradecirte, en 2 o 3 frases.", style_body))
    bloque_preguntas(story, "PREGUNTAS TRAMPA", "El oficial busca inconsistencias — mantén la calma", TRAMPA, RED, REDBG, es_trampa=True)
    story.append(PageBreak())

    story.append(Paragraph("CHECKLIST DE DOCUMENTOS", style_eyebrow))
    story.append(Paragraph("Lo que debes llevar a tu entrevista", style_h2))
    story.append(Spacer(1, 2 * mm))
    story.append(grupo_header("DOCUMENTOS OBLIGATORIOS", "Sin estos no puedes presentarte a la cita", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    for num, titulo, desc in OBLIG:
        story.append(doc_item(num, titulo, desc, GOLD2))
    story.append(Spacer(1, 5 * mm))
    story.append(grupo_header("DOCUMENTOS DE TRABAJO Y ESTUDIOS", "Respaldan tu arraigo en Ecuador", BLUE, BLUEBG))
    story.append(Spacer(1, 2 * mm))
    for num, titulo, desc in LABORALES:
        story.append(doc_item(num, titulo, desc, BLUE))
    story.append(Spacer(1, 5 * mm))
    story.append(grupo_header("VIAJE Y RESPALDO ADICIONAL", "Completan tu expediente para la entrevista", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    for num, titulo, desc in ADICIONAL:
        story.append(doc_item(num, titulo, desc, GOLD2))
    story.append(PageBreak())

    story.append(Paragraph("ULTIMO PASO", style_eyebrow))
    story.append(Paragraph("El día de tu cita", style_h2))
    story.append(Paragraph(
        "Tu cita es el <b>lunes 30 de noviembre de 2026, 8:30 AM</b> en el Consulado General de EE.UU. en Guayaquil (Calle Santa Ana y Av. José Rodríguez Bonín, sector San Eduardo). "
        "Lleva la confirmación del DS-160 con el código de barras que corresponde a tu cita y tu pasaporte.", style_body))
    story.append(Spacer(1, 3 * mm))
    story.append(strength_box("", "No llegues más de 15 minutos antes", "Solo se permite el ingreso a tu hora programada: no hay necesidad de llegar antes."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("", "Vestimenta formal", "Como para una reunión importante — comunica seriedad."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("", "Qué llevar", "Pasaporte original, confirmación DS-160 impresa, página de confirmación de cita, comprobante de pago MRV, foto, cédula y los documentos de respaldo de tu trabajo, tus estudios y quien paga el viaje."))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box("", "Qué NO llevar", "Celular (no pasa seguridad), laptop, tablet, cables, comida o bebidas."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("", "Dentro de la entrevista", "Responde solo lo que te preguntan, habla claro y sin apresurarte. Si preguntan por tu negativa de 2023, responde con calma y con la verdad: qué cambió desde entonces. Viajas cinco días de vacaciones y regresas a tu trabajo y a tu universidad."))
    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="100%", color=LINE, thickness=1))
    story.append(Spacer(1, 6 * mm))
    story.append(closing_band())
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF generado: {OUT_PATH}")


if __name__ == "__main__":
    build()
