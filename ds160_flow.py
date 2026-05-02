from ds160_preguntas import PREGUNTAS, GRUPOS
from datetime import datetime

# Sesiones activas: phone -> DS160Session
sesiones = {}

ADMIN_PHONE = "593994442512"  # Roberto recibe el reporte aquí


def get_grupo_info(grupo_id):
    for g in GRUPOS:
        if g["id"] == grupo_id:
            return g
    return None


class DS160Session:
    def __init__(self, phone):
        self.phone = phone
        self.fase = "inicio"          # inicio → nombres_personas → recopilando → completo
        self.personas = []            # ["Juan García", "Ana García", ...]
        self.persona_idx = 0          # persona actual
        self.pregunta_idx = 0         # pregunta actual dentro de PREGUNTAS
        self.datos = []               # [{"campo": "valor", ...}, ...]
        self.ultimo_grupo = None
        self.num_personas_esperado = 0

    def total_preguntas(self):
        return len(PREGUNTAS)

    def persona_actual(self):
        if self.persona_idx < len(self.personas):
            return self.personas[self.persona_idx]
        return "Viajero"

    def progreso(self):
        p = self.pregunta_idx + 1
        t = self.total_preguntas()
        bloques = int((p / t) * 10)
        barra = "█" * bloques + "░" * (10 - bloques)
        pct = int((p / t) * 100)
        return f"{barra} {pct}%  (pregunta {p}/{t})"

    def get_pregunta(self):
        if self.pregunta_idx < len(PREGUNTAS):
            return PREGUNTAS[self.pregunta_idx]
        return None

    def guardar_respuesta(self, respuesta):
        pregunta = self.get_pregunta()
        if pregunta and self.persona_idx < len(self.datos):
            self.datos[self.persona_idx][pregunta["campo"]] = respuesta
        self.pregunta_idx += 1

    def siguiente_mensaje(self, respuesta_anterior=None):
        """Devuelve el próximo mensaje a enviar al usuario."""

        # ── FASE INICIO ──────────────────────────────────────────
        if self.fase == "inicio":
            self.fase = "cuantos"
            return (
                "¡Hola! Voy a ayudarte a recopilar toda la información para el formulario *DS-160* de visa USA. "
                "Es más fácil de lo que parece — lo hacemos en partes pequeñas. 😊\n\n"
                "¿*Cuántas personas* van a viajar? (incluyéndote a ti)\n\n"
                "_(Ej: 4)_"
            )

        # ── FASE: CUÁNTAS PERSONAS ────────────────────────────────
        if self.fase == "cuantos":
            try:
                n = int(respuesta_anterior.strip())
                if n < 1 or n > 10:
                    return "Por favor escribe un número entre 1 y 10. ¿Cuántas personas van a viajar?"
                self.num_personas_esperado = n
                self.fase = "nombres"
                self.personas_temp = []
                return (
                    f"Perfecto, son *{n} persona{'s' if n > 1 else ''}*. "
                    f"Voy a recopilar la información de cada una.\n\n"
                    f"Dime el *nombre completo de la persona 1* (la que solicita la visa):"
                )
            except Exception:
                return "Escribe solo el número de personas. ¿Cuántas van a viajar?"

        # ── FASE: RECOPILAR NOMBRES ───────────────────────────────
        if self.fase == "nombres":
            self.personas_temp.append(respuesta_anterior.strip())
            if len(self.personas_temp) < self.num_personas_esperado:
                siguiente = len(self.personas_temp) + 1
                return f"Anotado ✓\n\n¿Nombre completo de la *persona {siguiente}*?"
            else:
                # Tenemos todos los nombres
                self.personas = self.personas_temp
                self.datos = [{} for _ in self.personas]
                self.fase = "recopilando"
                self.persona_idx = 0
                self.pregunta_idx = 0
                self.ultimo_grupo = None
                lista = "\n".join([f"  {i+1}. {p}" for i, p in enumerate(self.personas)])
                return (
                    f"Perfecto. Voy a recopilar datos de:\n{lista}\n\n"
                    f"Empezamos con *{self.personas[0]}*. ¡Vamos! 🚀\n\n"
                    + self._siguiente_pregunta()
                )

        # ── FASE: RECOPILANDO ─────────────────────────────────────
        if self.fase == "recopilando":
            if respuesta_anterior is not None:
                self.guardar_respuesta(respuesta_anterior.strip())

            # ¿Terminó esta persona?
            if self.pregunta_idx >= len(PREGUNTAS):
                self.persona_idx += 1
                self.pregunta_idx = 0
                self.ultimo_grupo = None

                # ¿Terminaron todas las personas?
                if self.persona_idx >= len(self.personas):
                    self.fase = "completo"
                    return None  # señal de completado

                nombre_sig = self.personas[self.persona_idx]
                return (
                    f"✅ *¡Listo con {self.personas[self.persona_idx - 1]}!*\n\n"
                    f"Ahora vamos con *{nombre_sig}*. Mismas preguntas, diferente persona.\n\n"
                    + self._siguiente_pregunta()
                )

            return self._siguiente_pregunta()

        return None

    def _siguiente_pregunta(self):
        pregunta = self.get_pregunta()
        if not pregunta:
            return None

        msgs = []

        # ¿Cambió de grupo? Mostrar cabecera del grupo
        grupo_actual = pregunta["grupo"]
        if grupo_actual != self.ultimo_grupo:
            self.ultimo_grupo = grupo_actual
            info = get_grupo_info(grupo_actual)
            if info:
                msgs.append(
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"{info['emoji']} *{info['titulo']}*\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"_{info['intro']}_"
                )

        # Progreso
        progreso_txt = self.progreso()

        # La pregunta
        nombre = self.persona_actual()
        pregunta_txt = pregunta["texto"]

        msgs.append(f"📋 {progreso_txt}\n\n*{nombre}* — {pregunta_txt}")

        return "\n\n".join(msgs)

    def generar_reporte(self):
        """Genera el reporte final formateado para Roberto."""
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
        lineas = [
            f"📋 *DS-160 — DATOS COMPLETOS*",
            f"📅 {ahora}",
            f"👥 {len(self.personas)} persona(s)",
            f"{'═' * 35}",
        ]

        for i, nombre in enumerate(self.personas):
            datos = self.datos[i]
            lineas.append(f"\n{'━' * 35}")
            lineas.append(f"👤 PERSONA {i+1}: {nombre.upper()}")
            lineas.append(f"{'━' * 35}")

            grupo_anterior = None
            for pregunta in PREGUNTAS:
                grupo = pregunta["grupo"]
                if grupo != grupo_anterior:
                    info = get_grupo_info(grupo)
                    if info:
                        lineas.append(f"\n{info['emoji']} {info['titulo'].upper()}")
                    grupo_anterior = grupo
                campo = pregunta["campo"]
                valor = datos.get(campo, "—")
                lineas.append(f"• {campo}: {valor}")

        lineas.append(f"\n{'═' * 35}")
        lineas.append(f"✅ Formulario completado. Listo para ingresar al DS-160.")
        return "\n".join(lineas)

    def reporte_por_bloques(self):
        """Divide el reporte en partes de max 3000 chars para WhatsApp."""
        reporte_completo = self.generar_reporte()
        bloques = []
        while len(reporte_completo) > 3000:
            corte = reporte_completo.rfind("\n", 0, 3000)
            if corte == -1:
                corte = 3000
            bloques.append(reporte_completo[:corte])
            reporte_completo = reporte_completo[corte:]
        if reporte_completo.strip():
            bloques.append(reporte_completo)
        return bloques


def procesar_mensaje_ds160(phone, mensaje):
    """
    Retorna lista de mensajes a enviar.
    Si retorna None, la sesión terminó.
    """
    session = sesiones.get(phone)

    # Iniciar nueva sesión
    if session is None:
        session = DS160Session(phone)
        sesiones[phone] = session

    respuesta = mensaje if session.fase not in ("inicio",) else None

    if session.fase == "inicio":
        msg = session.siguiente_mensaje()
        return [msg]

    msg = session.siguiente_mensaje(mensaje)

    if session.fase == "completo":
        return None  # señal de que completó

    if msg:
        return [msg]

    return []


def esta_en_sesion_ds160(phone):
    s = sesiones.get(phone)
    return s is not None and s.fase != "completo"


def iniciar_sesion_ds160(phone):
    sesiones[phone] = DS160Session(phone)
    return DS160Session(phone).siguiente_mensaje()


def obtener_reporte(phone):
    s = sesiones.get(phone)
    if s and s.fase == "completo":
        return s.reporte_por_bloques()
    return None


def obtener_todos_los_datos():
    """Para el endpoint admin — devuelve todas las sesiones completas."""
    resultado = []
    for phone, session in sesiones.items():
        if session.fase == "completo":
            resultado.append({
                "phone": phone,
                "personas": session.personas,
                "reporte": session.generar_reporte()
            })
    return resultado


def cancelar_sesion(phone):
    if phone in sesiones:
        del sesiones[phone]
