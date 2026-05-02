from schengen_preguntas import PREGUNTAS_SCHENGEN, GRUPOS_SCHENGEN
from datetime import datetime

sesiones_schengen = {}


def get_grupo_info(grupo_id):
    for g in GRUPOS_SCHENGEN:
        if g["id"] == grupo_id:
            return g
    return None


class SchengenSession:
    def __init__(self, phone):
        self.phone = phone
        self.fase = "inicio"
        self.personas = []
        self.persona_idx = 0
        self.pregunta_idx = 0
        self.datos = []
        self.ultimo_grupo = None
        self.num_personas_esperado = 0

    def total_preguntas(self):
        return len(PREGUNTAS_SCHENGEN)

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
        if self.pregunta_idx < len(PREGUNTAS_SCHENGEN):
            return PREGUNTAS_SCHENGEN[self.pregunta_idx]
        return None

    def guardar_respuesta(self, respuesta):
        pregunta = self.get_pregunta()
        if pregunta and self.persona_idx < len(self.datos):
            self.datos[self.persona_idx][pregunta["campo"]] = respuesta
        self.pregunta_idx += 1

    def siguiente_mensaje(self, respuesta_anterior=None):
        if self.fase == "inicio":
            self.fase = "cuantos"
            return (
                "Perfecto, voy a recopilar los datos para el formulario de *Visa Schengen*. "
                "Lo hacemos en partes, es sencillo. 😊\n\n"
                "¿*Cuántas personas* van a solicitar la visa?\n\n_(Ej: 2)_"
            )

        if self.fase == "cuantos":
            try:
                n = int(respuesta_anterior.strip())
                if n < 1 or n > 10:
                    return "Por favor escribe un número entre 1 y 10. ¿Cuántas personas?"
                self.num_personas_esperado = n
                self.fase = "nombres"
                self.personas_temp = []
                return (
                    f"Perfecto, son *{n} persona{'s' if n > 1 else ''}*.\n\n"
                    f"Dime el *nombre completo de la persona 1*:"
                )
            except Exception:
                return "Escribe solo el número. ¿Cuántas personas van a solicitar la visa?"

        if self.fase == "nombres":
            self.personas_temp.append(respuesta_anterior.strip())
            if len(self.personas_temp) < self.num_personas_esperado:
                siguiente = len(self.personas_temp) + 1
                return f"Anotado ✓\n\n¿Nombre completo de la *persona {siguiente}*?"
            else:
                self.personas = self.personas_temp
                self.datos = [{} for _ in self.personas]
                self.fase = "recopilando"
                self.persona_idx = 0
                self.pregunta_idx = 0
                self.ultimo_grupo = None
                lista = "\n".join([f"  {i+1}. {p}" for i, p in enumerate(self.personas)])
                return (
                    f"Perfecto. Voy a recopilar datos de:\n{lista}\n\n"
                    f"Empezamos con *{self.personas[0]}*. 🚀\n\n"
                    + self._siguiente_pregunta()
                )

        if self.fase == "recopilando":
            if respuesta_anterior is not None:
                self.guardar_respuesta(respuesta_anterior.strip())

            if self.pregunta_idx >= len(PREGUNTAS_SCHENGEN):
                self.persona_idx += 1
                self.pregunta_idx = 0
                self.ultimo_grupo = None

                if self.persona_idx >= len(self.personas):
                    self.fase = "completo"
                    return None

                nombre_sig = self.personas[self.persona_idx]
                return (
                    f"✅ *Listo con {self.personas[self.persona_idx - 1]}!*\n\n"
                    f"Ahora vamos con *{nombre_sig}*.\n\n"
                    + self._siguiente_pregunta()
                )

            return self._siguiente_pregunta()

        return None

    def _siguiente_pregunta(self):
        pregunta = self.get_pregunta()
        if not pregunta:
            return None

        msgs = []
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

        nombre = self.persona_actual()
        pregunta_txt = pregunta["texto"]
        msgs.append(f"📋 {self.progreso()}\n\n*{nombre}* — {pregunta_txt}")
        return "\n\n".join(msgs)

    def generar_reporte(self):
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
        lineas = [
            f"📋 *SCHENGEN — DATOS COMPLETOS*",
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
            for pregunta in PREGUNTAS_SCHENGEN:
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
        lineas.append(f"✅ Datos Schengen completados.")
        return "\n".join(lineas)

    def reporte_por_bloques(self):
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


def esta_en_sesion_schengen(phone):
    s = sesiones_schengen.get(phone)
    return s is not None and s.fase != "completo"


def iniciar_sesion_schengen(phone):
    session = SchengenSession(phone)
    sesiones_schengen[phone] = session
    return session.siguiente_mensaje()


def procesar_mensaje_schengen(phone, mensaje):
    session = sesiones_schengen.get(phone)
    if session is None:
        session = SchengenSession(phone)
        sesiones_schengen[phone] = session

    if session.fase == "inicio":
        return [session.siguiente_mensaje()]

    msg = session.siguiente_mensaje(mensaje)

    if session.fase == "completo":
        return None

    if msg:
        return [msg]
    return []


def obtener_reporte_schengen(phone):
    s = sesiones_schengen.get(phone)
    if s and s.fase == "completo":
        return s.reporte_por_bloques()
    return None


def cancelar_sesion_schengen(phone):
    if phone in sesiones_schengen:
        del sesiones_schengen[phone]


def obtener_datos_sesion_schengen(phone):
    s = sesiones_schengen.get(phone)
    if s and s.fase == "completo":
        return s.personas, s.datos
    return [], []
