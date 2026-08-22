"""
Genera pdf-karen-beltran.pdf -- Guia personalizada + checklist + preguntas
Visa B1/B2 USA -- Karen Pamela Beltran Brito
Cita: PENDIENTE de asignacion por el consulado (DS-160 enviado 21-ago-2026)
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

CLIENTE = "Karen Beltran"
CLIENTE_COMPLETO = "Karen Pamela Beltran Brito"
DESTINO = "Miami, EE.UU."
FECHA_CITA = "28 sept 2026, 8:00 AM (TENTATIVA — a confirmar)"
LUGAR_CITA = "Embajada de EE.UU. en Quito"
DS160 = "AA00FQT5BD"
PASAPORTE = "A9657309"

OUT_PATH = os.path.join(os.path.dirname(__file__), "pdf-karen-beltran.pdf")

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
        f"<font size=12 color='#1E293B'><b>{FECHA_CITA}</b></font><br/>"
        f"<font size=9 color='#475569'>{LUGAR_CITA}</font>",
        ParagraphStyle("box", parent=style_body, leading=14, spaceAfter=0)
    )
    right = Paragraph(
        "<font size=8 color='#C2410C'><b>DS-160 / PASAPORTE</b></font><br/>"
        f"<font size=12 color='#1E293B'><b>{DS160}</b></font><br/>"
        f"<font size=9 color='#475569'>{PASAPORTE} · vence 20 may 2033</font>",
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
        "<font color='#FFFFFF' size=13><b>Gracias por confiar tu proceso en nosotros, Karen.</b></font><br/>"
        "<font color='#94A3B8' size=9>En cuanto el consulado asigne tu fecha te avisamos de inmediato — "
        "mientras tanto, estamos a un mensaje de WhatsApp de distancia.</font>",
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
     "Sea directa: viaje de negocios/turismo corto, 3 dias, a Miami.",
     "Viajo a Miami por un motivo de negocios y turismo, del 25 al 28 de septiembre de 2026. Es un viaje corto, de tres dias."),
    ("¿A qué se dedica usted?",
     "Cargo actual en ISA Garcia LLC, coordinacion de comunicaciones operativas.",
     "Trabajo en Isa Garcia LLC, donde coordino comunicaciones operativas, ciclos de lanzamiento de programas y la relacion con proveedores y aliados comerciales."),
    ("¿Cuánto tiempo se va a quedar?",
     "Fechas exactas del DS-160: 25 al 28 de septiembre, 3 dias.",
     "Tres dias. Llego a Miami el 25 de septiembre y regreso a Ecuador el 28 de septiembre de 2026."),
    ("¿Dónde se va a hospedar?",
     "439 Northwest 4th Avenue, Miami, Florida.",
     "Me hospedo en el 439 de la Northwest 4th Avenue, en Miami, Florida. Ya tengo la direccion confirmada."),
    ("¿Tiene familiares en los Estados Unidos?",
     "No tiene ningun familiar en USA. Respuesta directa.",
     "No, no tengo ningun familiar en los Estados Unidos."),
]

INTERMEDIAS = [
    ("¿Cuánto gana usted en su trabajo actual?",
     "$2,600 mensuales exactos, segun lo declarado en el DS-160.",
     "Dos mil seiscientos dolares mensuales, como parte de mi rol en Isa Garcia LLC."),
    ("¿Ha viajado antes fuera de Ecuador?",
     "Si, a Peru, Colombia, Republica Dominicana, Bolivia, Chile y Brasil en los ultimos 5 anos.",
     "Si, he viajado a Peru, Colombia, Republica Dominicana, Bolivia, Chile y Brasil en los ultimos cinco anos, y regrese a Ecuador sin ningun inconveniente en todos los casos."),
    ("¿Es soltera? ¿Tiene hijos?",
     "Soltera, sin hijos — el arraigo se sustenta en trayectoria laboral y familia (padres) en Ecuador.",
     "Si, soy soltera y no tengo hijos. Mi arraigo esta en mi trayectoria profesional de mas de siete anos y en mi familia, mis padres, que viven en Quito."),
    ("¿Cuánto tiempo lleva trabajando en su empleo actual?",
     "Reciente — antes trabajo 7+ anos en Telefonica Movistar (2018-2025).",
     "En mi rol actual llevo un tiempo corto, pero antes trabaje mas de siete anos en Telefonica Movistar Ecuador, en el area de marketing, hasta junio de 2025."),
    ("¿Es la primera vez que solicita una visa a Estados Unidos?",
     "Si, primer viaje a USA, sin rechazos previos.",
     "Si, es mi primera solicitud de visa a Estados Unidos. No tengo rechazos previos de ningun tipo."),
]

DIFICILES = [
    ("¿Por qué viaja a Miami si trabaja para una empresa de Miami?",
     "Ancla principal: es parte del equipo (remoto, desde Ecuador), pero este viaje puntual es por invitacion al evento presencial, con fechas exactas que coinciden con el viaje declarado.",
     "Trabajo de forma remota para Isa Garcia Corp desde Ecuador. Este viaje puntual es porque fui invitada a participar en su evento presencial 'Ella Empresaria', el 26 y 27 de septiembre en Miami Beach — es una participacion como invitada al evento, no un traslado laboral."),
    ("Su contacto en Estados Unidos es la misma empresa para la que usted trabaja — ¿por qué?",
     "Es coherente: es su empleadora remota Y la organizadora del evento al que fue invitada; aclarar que no implica reubicacion.",
     "Isabel Garcia dirige la empresa para la que trabajo de forma remota desde Ecuador, y tambien es quien organiza el evento 'Ella Empresaria' al que fui invitada como participante. La declare como contacto porque es con quien coordino mi visita."),
    ("¿Por qué un viaje de solo tres días?",
     "El evento dura exactamente 2 dias (26-27 sept), el viaje declarado (25-28 sept) incluye llegada y salida — coincide perfecto, evidencia concreta del motivo real.",
     "Porque el evento al que fui invitada dura dos dias, el 26 y 27 de septiembre. Mi viaje es del 25 al 28 para tener margen de llegada y salida, nada mas."),
    ("¿Qué garantía tengo de que usted regresará a Ecuador?",
     "7+ años de trayectoria laboral en Ecuador, estudios en Ecuador y España (siempre regreso), múltiples viajes previos con retorno comprobado, padres en Ecuador.",
     "Tengo mas de siete años de trayectoria laboral en Ecuador, hice una maestria en España y regrese a completar mi carrera aqui, y he viajado a seis países en los últimos cinco años, siempre regresando a Ecuador. Mis padres tambien viven aqui."),
    ("¿Por qué estudió en España y no se quedó allá?",
     "Regreso a Ecuador tras la maestria (jul 2024) — patron de retorno consistente.",
     "Hice mi maestria en Marketing Digital y Analitica en la Universidad Internacional de Valencia, y al terminar en julio de 2024 regrese a Ecuador para continuar mi carrera profesional aqui."),
]

TRAMPA = [
    ("¿Ha sufrido daños, violencia o maltrato en su país de origen o en su última residencia habitual?",
     "CRÍTICA — pregunta obligatoria 2026 para detectar posibles solicitantes de asilo. Un 'sí' puede derivar en negativa automática.",
     "No, nunca he sufrido daños, violencia ni maltrato en Ecuador. Vivo y trabajo con normalidad en mi país."),
    ("¿Teme sufrir daños, persecución o maltrato si regresa a ese país?",
     "CRÍTICA — segunda pregunta obligatoria 2026. No tiene motivo real para temer volver.",
     "No, no tengo ningún temor de regresar a Ecuador. Es mi país, donde vivo y trabajo."),
    ("¿Por qué debería darle la visa a usted y no a cualquier otra persona?",
     "La ley (Sección 214(b)) presume que todo solicitante quiere quedarse — demuéstrelo con hechos, sin sonar a súplica.",
     "Porque tengo un caso solido: trayectoria laboral de mas de siete años en Ecuador, estudios completados aqui y en España con retorno comprobado, y un historial de seis viajes internacionales previos, siempre regresando a mi país."),
    ("Usted trabaja para una empresa de Miami y viaja a Miami — ¿no es esto en realidad un traslado laboral disfrazado de turismo?",
     "Niegue con seguridad: ya trabaja remota desde Ecuador (eso no cambia), el viaje es puntual por invitacion a un evento con fecha fija, sin intencion de trabajar fisicamente en EE.UU. ni de reubicarse.",
     "No. Ya trabajo de forma remota para esta empresa desde Ecuador, donde vivo, y eso no va a cambiar. Este viaje es una visita corta y puntual de tres dias porque fui invitada a un evento presencial especifico, el 26 y 27 de septiembre. No es un traslado ni una solicitud de empleo en Estados Unidos."),
    ("¿Planea buscar trabajo o quedarse a vivir en Estados Unidos durante este viaje?",
     "No contemple esa opcion ni siquiera hipoteticamente — reafirme la obligacion de regreso.",
     "No, no es algo que contemple. Mi vida, mi trabajo y mi familia estan en Ecuador, y mi vuelo de regreso ya esta fijado para el 28 de septiembre."),
    ("¿Cómo puede pagar sus gastos siendo soltera y sin ingresos altos declarados?",
     "Ingreso de $2,600/mes es estable; viaje corto de 3 dias reduce el costo total — responda con seguridad sin sobre-explicar.",
     "Tengo un ingreso mensual estable de dos mil seiscientos dolares, y este es un viaje corto de solo tres dias, por lo que puedo cubrir todos mis gastos sin inconveniente."),
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
    story.append(Paragraph("Motivo de viaje: negocios/turismo — invitada a evento en Miami", style_h2))
    story.append(Paragraph(
        "Viajas del <b>25 al 28 de septiembre de 2026</b> a Miami. Trabajas de forma remota desde Ecuador "
        "para Isa Garcia Corp, y fuiste invitada a participar en su evento presencial <b>'Ella Empresaria'</b> "
        "(26-27 de septiembre, Miami Beach) — tu contacto declarado en EE.UU. es Isabel Garcia, quien dirige "
        "la empresa y organiza el evento. Te hospedas en 439 Northwest 4th Avenue, Miami, Florida.",
        style_body
    ))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("FORTALEZAS DE TU CASO", style_eyebrow))
    story.append(strength_box("✔", "Trayectoria laboral solida",
        "Mas de 7 años en Telefonica Movistar Ecuador (2018-2025) antes de su rol actual — historial "
        "laboral continuo y verificable en Ecuador."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("✔", "Historial de viajes con retorno comprobado",
        "6 paises visitados en los ultimos 5 anos (Peru, Colombia, Rep. Dominicana, Bolivia, Chile, Brasil), "
        "siempre regresando a Ecuador."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("✔", "Estudios en Ecuador y España, con retorno",
        "Maestria en la Universidad Internacional de Valencia (2023-2024) — regreso a Ecuador al terminar."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("✔", "Fechas exactas y verificables",
        "El evento 'Ella Empresaria' dura del 26 al 27 de septiembre — coincide exactamente con tu viaje "
        "(25-28 sept), evidencia concreta de que el motivo real es asistir al evento como invitada."))
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("PUNTOS A PREPARAR CON CALMA", style_eyebrow))
    story.append(risk_box("⚠", "Empleadora con domicilio en Miami",
        "Explica siempre que tu relacion laboral con Isa Garcia Corp es remota, desde Ecuador, y que este "
        "viaje puntual es por ser invitada al evento presencial, no por trabajar fisicamente en EE.UU."))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box("⚠", "Contacto en EE.UU. es tu propia empleadora",
        "Es honesto y normal: es tu empleadora remota y quien organiza el evento al que fuiste invitada — "
        "aclara que es una participacion puntual como invitada, no una mudanza ni un nuevo empleo presencial."))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box("⚠", "Soltera, sin hijos",
        "Tu arraigo se sustenta en tu trayectoria laboral (7+ años), tus estudios y tus padres en Ecuador — "
        "apoyate en esos puntos, no te disculpes por no tener hijos."))

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
    bloque_preguntas(story, "NIVEL DIFICIL", "Aqui es donde se decide la entrevista — el punto clave: por que viajas si tu empresa esta en Miami",
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
        ("1", "Pasaporte vigente", f"Numero {PASAPORTE}, vence 20 de mayo de 2033."),
        ("2", "Confirmacion DS-160", f"Codigo de barras legible, numero {DS160}."),
        ("3", "Pagina de confirmacion e instrucciones de la cita",
         "Impresa desde ais.usvisa-info.com en cuanto el consulado asigne la fecha."),
        ("4", "Fotografia 5x5 cm a color",
         "Tomada dentro de los ultimos 6 meses, fondo claro."),
        ("5", "Comprobante de pago de la tasa MRV",
         "Guardalo impreso — puede ser solicitado en la entrevista."),
        ("6", "Cedula de identidad", "Copia y original, como respaldo adicional de identidad."),
    ]
    for num, titulo, desc in obligatorios:
        story.append(doc_item(num, titulo, desc, GOLD2))
    story.append(Spacer(1, 5 * mm))
    story.append(grupo_header("DOCUMENTOS LABORALES Y DEL EVENTO", "Respaldan tu empleo remoto y tu invitacion al evento en Miami", BLUE, BLUEBG))
    story.append(Spacer(1, 2 * mm))
    laborales = [
        ("7", "Carta laboral de Isa Garcia Corp",
         "Que indique cargo, fecha de inicio, salario y que el trabajo es remoto desde Ecuador."),
        ("8", "Comprobante de inscripcion/invitacion al evento 'Ella Empresaria'",
         "Confirmacion de participacion como invitada, con las fechas 26-27 de septiembre 2026."),
        ("9", "3 ultimos comprobantes de pago / transferencias",
         "Que demuestren el ingreso mensual declarado de $2,600."),
        ("10", "Certificado laboral de Telefonica Movistar Ecuador",
         "Respalda los 7+ años de trayectoria previa (2018-2025)."),
        ("11", "Certificado de la maestria en la Universidad Internacional de Valencia",
         "Respalda el periodo de estudios en España y el regreso a Ecuador."),
    ]
    for num, titulo, desc in laborales:
        story.append(doc_item(num, titulo, desc, BLUE))
    story.append(Spacer(1, 5 * mm))
    story.append(grupo_header("VIAJE Y RESPALDO ADICIONAL", "Completan tu expediente para la entrevista", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    adicional = [
        ("11", "Reserva de alojamiento",
         "439 Northwest 4th Avenue, Miami, Florida, confirmada del 25 al 28 de septiembre."),
        ("12", "Itinerario de vuelo (ida y vuelta)",
         "Confirma la fecha de regreso fija, 28 de septiembre de 2026."),
        ("13", "Seguro de viaje / asistencia medica internacional",
         "Cobertura para todo el periodo del viaje."),
        ("14", "Estados de cuenta bancarios recientes",
         "Refuerzan la solvencia para cubrir gastos del viaje."),
        ("15", "Sellos de pasaporte de viajes previos",
         "Peru, Colombia, Rep. Dominicana, Bolivia, Chile y Brasil — evidencia de retorno consistente."),
    ]
    for num, titulo, desc in adicional:
        story.append(doc_item(num, titulo, desc, GOLD2))

    story.append(PageBreak())

    # ── PAGINA 5 — Protocolo del dia de la cita ─────────────────────────
    story.append(Paragraph("ULTIMO PASO", style_eyebrow))
    story.append(Paragraph("El dia de tu cita", style_h2))
    story.append(Paragraph(
        f"Tu cita esta <b>{FECHA_CITA}</b> en la {LUGAR_CITA} "
        "(Avenida Avigiras E12-170 y Eloy Alfaro, Quito). Te avisaremos apenas el consulado asigne la fecha exacta.",
        style_body
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(strength_box("📍", "Llega 20-30 minutos antes",
        "No mas de 15 minutos antes de tu hora exacta — no hay necesidad de llegar mucho antes."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("👔", "Vestimenta formal",
        "Como para una reunion de trabajo importante — comunica seriedad profesional."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("🎒", "Que llevar",
        "Pasaporte original, confirmacion DS-160 impresa, pagina de confirmacion de cita, "
        "comprobante de pago MRV, foto y documentos de respaldo laboral."))
    story.append(Spacer(1, 2 * mm))
    story.append(risk_box("🚫", "Que NO llevar",
        "Celular (no pasa seguridad), laptop, tablet, cables, comida o bebidas."))
    story.append(Spacer(1, 2 * mm))
    story.append(strength_box("💬", "Dentro de la entrevista",
        "Responde solo lo que te preguntan, habla claro y sin apresurarte. Si preguntan por tu "
        "empleadora en Miami, explica una sola vez que tu trabajo es remoto desde Ecuador y que este viaje es "
        "por ser invitada al evento 'Ella Empresaria', y sigue adelante — no te justifiques en exceso."))

    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="100%", color=LINE, thickness=1))
    story.append(Spacer(1, 6 * mm))
    story.append(closing_band())

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF generado: {OUT_PATH}")


if __name__ == "__main__":
    build()
