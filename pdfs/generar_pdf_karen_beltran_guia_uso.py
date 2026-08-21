"""
Genera pdf-karen-beltran-guia-uso.pdf -- Como usar el simulador (instrucciones de navegacion)
Visa B1/B2 USA -- Jennifer Paola Samaniego Marines
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
GREEN    = colors.HexColor("#10B981")
GREENBG  = colors.HexColor("#F0FDF4")
RED      = colors.HexColor("#EF4444")
REDBG    = colors.HexColor("#FEF2F2")
BLUE     = colors.HexColor("#3B82F6")
BLUEBG   = colors.HexColor("#EFF6FF")
SLATEBG  = colors.HexColor("#F8FAFC")
LINE     = colors.HexColor("#E2E8F0")

CLIENTE = "Karen Beltran"
SIMULADOR_URL = "asesoriadevisadosglobal.com/karen-beltran.html"

OUT_PATH = os.path.join(os.path.dirname(__file__), "pdf-karen-beltran-guia-uso.pdf")

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
    canvas.drawString(20 * mm, height - 18 * mm, "COMO USAR TU SIMULADOR DE ENTREVISTA")

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 17)
    canvas.drawString(20 * mm, height - 27 * mm, f"Guia de uso — {CLIENTE}")

    cx, cy = width - 18 * mm, height - 16 * mm
    canvas.setFillColor(GOLD)
    canvas.circle(cx, cy, 9 * mm, stroke=0, fill=1)
    canvas.setFillColor(NAVY)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawCentredString(cx, cy - 2 * mm, str(canvas.getPageNumber()))
    canvas.setFont("Helvetica-Bold", 6.5)
    canvas.drawCentredString(cx, cy - 7 * mm, "DE 2")

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


def link_box():
    data = [[Paragraph(
        "<font size=8 color='#C2410C'><b>TU SIMULADOR PERSONALIZADO</b></font><br/>"
        f"<font size=13 color='#1E293B'><b>{SIMULADOR_URL}</b></font><br/>"
        "<font size=9 color='#475569'>Guardalo en favoritos — lo usaras todos los dias hasta tu entrevista.</font>",
        ParagraphStyle("box", parent=style_body, leading=14, spaceAfter=0))]]
    t = Table(data, colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF7ED")),
        ("BOX", (0, 0), (-1, -1), 1.2, colors.HexColor("#F59E0B")),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def paso_item(numero, titulo, descripcion, badge_color):
    badge = Table([[Paragraph(f"<b>{numero}</b>", ParagraphStyle(
                    "num", parent=style_body, textColor=colors.white,
                    fontSize=11, leading=13, alignment=TA_CENTER))]],
                  colWidths=[11 * mm], rowHeights=[11 * mm],
                  style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), badge_color),
                                     ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                     ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    content = Paragraph(f"<b>{titulo}</b><br/>{descripcion}", style_item_body)
    t = Table([[badge, content]], colWidths=[15 * mm, 155 * mm])
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


def tip_box(titulo, desc, color, bg):
    data = [[Paragraph(f"<b>{titulo}</b><br/>{desc}", style_item_body)]]
    t = Table(data, colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 4, color),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return t


def build():
    doc = SimpleDocTemplate(
        OUT_PATH, pagesize=A4,
        topMargin=38 * mm, bottomMargin=24 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm,
        title=f"Guia de uso del simulador - {CLIENTE}",
    )
    story = []

    story.append(Paragraph("PRIMEROS PASOS", style_eyebrow))
    story.append(Paragraph(f"Como usar tu simulador, {CLIENTE.split()[0]}", style_h2))
    story.append(Paragraph(
        "Tu simulador es una pagina web personalizada, hecha con los datos reales de tu DS-160. "
        "No necesitas instalar nada — se abre desde el navegador de tu celular o computadora, "
        "y guarda tu avance automaticamente cada vez que lo usas.",
        style_body
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(link_box())
    story.append(Spacer(1, 8 * mm))

    story.append(grupo_header("PASO A PASO", "Sigue este orden la primera vez que entres", GOLD2, GOLDBG))
    story.append(Spacer(1, 2 * mm))
    pasos = [
        ("1", "Abre el link en tu celular o computadora",
         "Se abre directo en el navegador (Chrome, Safari) — no hay que descargar nada."),
        ("2", "Lee la pantalla de bienvenida",
         "Muestra el resumen de tu caso: cita, datos del viaje y tus fortalezas principales."),
        ("3", 'Toca "Empezar preparación"',
         "Te lleva al paso de estudio, donde estan todas las preguntas con su respuesta modelo."),
        ("4", "Estudia cada pregunta con calma",
         "Lee la pregunta, el tip y la respuesta modelo de cada nivel: basico, intermedio, dificil y modo oficial consular."),
        ("5", 'Cuando te las sepas, toca "Ya me las sé — empezar práctica"',
         "Aqui ya NO se muestra la respuesta modelo — debes escribir la tuya, como en la entrevista real."),
        ("6", "Escribe tu respuesta y toca «Verificar»",
         "El sistema evalua tu respuesta y te dice si esta bien, que mejorar, o si hay riesgo."),
        ("7", "Avanza pregunta por pregunta y por nivel",
         "Basico → Intermedio → Dificil → Modo oficial consular (preguntas trampa, las mas exigentes)."),
    ]
    for num, titulo, desc in pasos:
        story.append(paso_item(num, titulo, desc, GOLD2))

    story.append(Spacer(1, 8 * mm))
    story.append(grupo_header("RECOMENDACIONES DE USO", "Para sacarle el maximo provecho", BLUE, BLUEBG))
    story.append(Spacer(1, 2 * mm))
    story.append(tip_box("Practica todos los dias, aunque sea 10-15 minutos",
        "La constancia importa mas que sesiones largas y espaciadas. Revisalo apenas recibas el correo diario.",
        BLUE, BLUEBG))
    story.append(Spacer(1, 2 * mm))
    story.append(tip_box("Responde en voz alta, no solo por escrito",
        "Practica diciendo tu respuesta en voz alta antes de escribirla — asi suena mas natural en la entrevista real.",
        BLUE, BLUEBG))
    story.append(Spacer(1, 2 * mm))
    story.append(tip_box("Repite los niveles que te resulten dificiles",
        "Al terminar cada nivel puedes tocar «Repetir este nivel» las veces que necesites.",
        BLUE, BLUEBG))
    story.append(Spacer(1, 2 * mm))
    story.append(tip_box('El "Modo oficial consular" es el mas importante',
        "Incluye las preguntas trampa y las 2 preguntas obligatorias 2026 — practicalo varias veces la ultima semana antes de tu cita.",
        RED, REDBG))

    story.append(Spacer(1, 8 * mm))
    data = [[Paragraph(
        "<font color='#065F46'><b>¿DUDAS CON EL SIMULADOR?</b></font><br/>"
        "<font color='#1E293B'>Escribenos por WhatsApp al <b>+593 98 784 6751</b> y te ayudamos directamente. "
        "Estamos contigo en cada paso hasta tu cita.</font>",
        ParagraphStyle("cta", parent=style_body, fontSize=10, leading=15, spaceAfter=0))]]
    t = Table(data, colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GREENBG),
        ("LINEBEFORE", (0, 0), (0, -1), 4, GREEN),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(t)

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF generado: {OUT_PATH}")


if __name__ == "__main__":
    build()
