"""
Genera pdf-joycet-alcivar-checklist.pdf -- Checklist de documentos standalone
Visa B1/B2 USA -- Joycet Alejandra Alcivar Alcivar
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER

NAVY     = colors.HexColor("#0A1E5A")
NAVY2    = colors.HexColor("#071A4D")
GOLD     = colors.HexColor("#C9A455")
GOLD2    = colors.HexColor("#B8873A")
GOLDBG   = colors.HexColor("#FFFBEB")
GREY     = colors.HexColor("#475569")
LIGHTGREY= colors.HexColor("#94A3B8")
DARK     = colors.HexColor("#1E293B")
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
TOTAL_PAGES = 2

FORTALEZAS = [('Trabajo actual estable', 'Cajera en Corporación La Favorita, con un salario declarado de $800 mensuales, y experiencia previa como asistente de ventas en Ultra UV (oct 2023 – mar 2025).'), ('Estudiante de Odontología', 'Cursas Odontología en la Universidad Bolivariana del Ecuador desde octubre de 2024: una carrera en marcha que te ata a Ecuador.'), ('Viaje corto y en familia', 'Cinco días de vacaciones en Orlando, viajando con tu mamá y tu familia, con hospedaje definido en The Point Hotel & Suites.'), ('Sin familiares ni contactos en EE.UU.', 'No tienes familiares inmediatos ni otros familiares en Estados Unidos, ni peticiones de inmigrante a tu nombre.'), ('Honestidad al declarar', 'Declaraste con claridad tu negativa de 2023 (214b). Eso suma credibilidad: lo importante es explicar con calma qué cambió desde entonces.'), ('Pasaporte vigente y un viaje previo con retorno', 'Pasaporte vigente hasta 2033 y un viaje a República Dominicana en los últimos 5 años, del que regresaste a Ecuador.')]
RIESGOS = [('Negativa 214(b) de agosto de 2023', 'Es el punto más importante: el oficial la verá en tu DS-160 y preguntará qué cambió. Responde breve y con calma: tenías 19 años, y desde entonces trabajas, estudias Odontología y tu vida está en Ecuador.'), ('Quien paga no es tu papá ni tu mamá', 'Armando Weir figura como «otro familiar». Ten clara tu relación con él, a qué se dedica y por qué paga el viaje; lleva su carta de respaldo y sus documentos. El DS-160 no trae su ocupación ni sus ingresos.'), ('Primera vez en EE.UU. y poco historial de viaje', 'Solo viajaste a República Dominicana. Se compensa con tu trabajo, tu carrera, tu familia en Ecuador y un viaje corto de cinco días.'), ('Perfil joven, soltera y con ingreso modesto', 'Tienes 22 años y un salario de $800. Por eso pesa tanto que el patrocinador tenga respaldo real y que tu trabajo y tu carrera estén claros y comprobables.'), ('Ocupación «Business» y fechas en tu DS-160', 'El formulario marca tu ocupación principal como «Business» (tu empleo real es cajera) y no trae la fecha de ingreso a La Favorita; la carrera figura con fin de asistencia el 1 de nov de 2026. Ten claras estas tres cosas y respóndelas con naturalidad.')]
OBLIG = [('1', 'Pasaporte vigente', 'Número A8518412, vence el 3 de enero de 2033.'), ('2', 'Confirmación DS-160', 'Código de barras legible, número AA00FX9FL5. Es el que coincide con tu cita: NO lleves el anterior (AA00FW66SV).'), ('3', 'Página de confirmación e instrucciones de la cita', 'Impresa desde ais.usvisa-info.com, con el código de barras de tu cita (lunes 30 de noviembre de 2026, 8:30 AM, Guayaquil).'), ('4', 'Fotografía 5x5 cm a color', 'Tomada dentro de los últimos 6 meses, fondo claro.'), ('5', 'Comprobante de pago de la tasa MRV', 'Guárdalo impreso — puede ser solicitado en la entrevista.'), ('6', 'Cédula de identidad', 'Original y copia, como respaldo adicional de identidad.')]
LABORALES = [('7', 'Certificado laboral de Corporación La Favorita', 'Cargo de cajera, fecha de ingreso, salario de $800 y, si es posible, confirmación de tus vacaciones para el 1 de marzo de 2027.'), ('8', 'Rol de pagos de los últimos 3 meses', 'Respalda el salario de $800 declarado en el DS-160.'), ('9', 'Historial de aportes al IESS', 'Muestra la continuidad de tu vida laboral desde 2023.'), ('10', 'Certificado laboral de Ultra UV', 'Asistente de ventas, del 2 de octubre de 2023 al 11 de marzo de 2025.'), ('11', 'Certificado de matrícula y de estudios', 'Universidad Bolivariana del Ecuador, Odontología: debe mostrar que sigues matriculada, tu ciclo y tu calendario académico.'), ('12', 'Estados de cuenta bancarios de 6 meses', 'Muestran movimiento coherente con tus ingresos.')]
ADICIONAL = [('13', 'Carta de respaldo económico de Armando Weir', 'Que indique que cubre los gastos del viaje, con su cédula y comprobantes de su ocupación e ingresos (rol de pagos o RUC y estados de cuenta).'), ('14', 'Documentos de parentesco', 'Partida de nacimiento tuya y los documentos que muestren tu relación con tu mamá y con los familiares que viajan contigo.'), ('15', 'Reserva de hospedaje', 'The Point Hotel & Suites, 7389 Universal Boulevard, Orlando, Florida 32819 — desde el 1 de marzo de 2027 (5 días).'), ('16', 'Cotización o reserva de vuelo ida y vuelta', 'Con la fecha de regreso a Ecuador. Cuidado: no compres tiquetes hasta tener la visa.'), ('17', 'Seguro de viaje / asistencia médica internacional', 'Cobertura para todo el periodo del viaje.'), ('18', 'Copias de pasaportes y visas de quienes viajan contigo', 'Tu mamá, Armando, Ashlyn y Clarissa: si alguno ya tiene visa de EE.UU., lleva la copia.')]

OUT_PATH = os.path.join(os.path.dirname(__file__), "pdf-joycet-alcivar-checklist.pdf")

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
    canvas.drawString(20 * mm, height - 18 * mm, "CHECKLIST DE DOCUMENTOS PARA TU CITA")

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 17)
    canvas.drawString(20 * mm, height - 27 * mm, f"Checklist B1/B2 USA — {CLIENTE}")

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
        f"<font size=13 color='#1E293B'><b>{FECHA_CITA}</b></font><br/>"
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
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF7ED")),
        ("BOX", (0, 0), (-1, -1), 1.2, colors.HexColor("#F59E0B")),
        ("LINEAFTER", (0, 0), (0, 0), 1, colors.HexColor("#FBBF24")),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def doc_item(numero, titulo, descripcion, badge_color):
    checkbox = Table([[""]], colWidths=[6.5 * mm], rowHeights=[6.5 * mm],
                      style=TableStyle([("BOX", (0, 0), (-1, -1), 1.3, LIGHTGREY),
                                         ("BACKGROUND", (0, 0), (-1, -1), colors.white)]))
    badge = Table([[Paragraph(f"<b>{numero}</b>", ParagraphStyle(
                    "num", parent=style_body, textColor=colors.white,
                    fontSize=8.5, leading=10, alignment=TA_CENTER))]],
                  colWidths=[10 * mm], rowHeights=[7 * mm],
                  style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), badge_color),
                                     ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                     ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    content = Paragraph(f"<b>{titulo}</b><br/>{descripcion}", style_item_body)
    t = Table([[checkbox, badge, content]], colWidths=[10 * mm, 13 * mm, 147 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 9),
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


def build():
    doc = SimpleDocTemplate(
        OUT_PATH, pagesize=A4,
        topMargin=38 * mm, bottomMargin=24 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm,
        title=f"Checklist B1/B2 USA - {CLIENTE}",
    )
    story = []

    story.append(Paragraph("CHECKLIST DE DOCUMENTOS", style_eyebrow))
    story.append(Paragraph(f"Todo lo que {CLIENTE.split()[0]} debe llevar a su entrevista", style_h2))
    story.append(Paragraph(
        "Marca cada casilla a medida que reunas los documentos. Los obligatorios son "
        "indispensables para presentarte a la cita; los de respaldo refuerzan tu caso "
        "y tu arraigo pero no son excluyentes.",
        style_body
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(cita_box())
    story.append(Spacer(1, 8 * mm))

    story.append(grupo_header("DOCUMENTOS PERSONALES OBLIGATORIOS", "Sin estos no puedes presentarte a la cita", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    for num, titulo, desc in OBLIG:
        story.append(doc_item(num, titulo, desc, GOLD2))

    story.append(Spacer(1, 6 * mm))
    story.append(grupo_header("DOCUMENTOS DE TRABAJO Y ESTUDIOS", "Respaldan tu arraigo en Ecuador", BLUE, BLUEBG))
    story.append(Spacer(1, 2 * mm))
    for num, titulo, desc in LABORALES:
        story.append(doc_item(num, titulo, desc, BLUE))

    story.append(Spacer(1, 6 * mm))
    story.append(grupo_header("VIAJE Y RESPALDO ADICIONAL", "Completan tu expediente para la entrevista", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    for num, titulo, desc in ADICIONAL:
        story.append(doc_item(num, titulo, desc, GOLD2))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF generado: {OUT_PATH}")


if __name__ == "__main__":
    build()
