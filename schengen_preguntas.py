GRUPOS_SCHENGEN = [
    {
        "id": "personal",
        "emoji": "👤",
        "titulo": "Datos Personales",
        "intro": "Empecemos con tus datos personales para el formulario Schengen."
    },
    {
        "id": "pasaporte",
        "emoji": "📘",
        "titulo": "Pasaporte",
        "intro": "Ahora los datos de tu pasaporte. Tenlo a mano."
    },
    {
        "id": "viaje",
        "emoji": "✈️",
        "titulo": "El Viaje",
        "intro": "Cuéntame sobre tu viaje a Europa."
    },
    {
        "id": "contacto",
        "emoji": "🏠",
        "titulo": "Contacto en Ecuador",
        "intro": "Tu información de contacto en Ecuador."
    },
    {
        "id": "trabajo",
        "emoji": "💼",
        "titulo": "Trabajo y Finanzas",
        "intro": "Información laboral y financiera — clave para el Schengen."
    },
    {
        "id": "historial",
        "emoji": "🗺️",
        "titulo": "Historial de Visas",
        "intro": "Historial de viajes y visas previas."
    },
]

PREGUNTAS_SCHENGEN = [
    # ══════════════════════════════════
    # GRUPO 1: DATOS PERSONALES
    # ══════════════════════════════════
    {
        "id": "apellidos",
        "grupo": "personal",
        "texto": "¿Cuáles son tus *apellidos* tal como aparecen en el pasaporte?",
        "campo": "Apellidos"
    },
    {
        "id": "nombres",
        "grupo": "personal",
        "texto": "¿Y tus *nombres completos* como están en el pasaporte?",
        "campo": "Nombres"
    },
    {
        "id": "fecha_nacimiento",
        "grupo": "personal",
        "texto": "¿Cuál es tu *fecha de nacimiento*?\n\n_(día/mes/año — Ej: 15/03/1988)_",
        "campo": "Fecha de nacimiento"
    },
    {
        "id": "lugar_nacimiento",
        "grupo": "personal",
        "texto": "¿En qué *ciudad y país naciste*?\n\n_(Ej: Guayaquil, Ecuador)_",
        "campo": "Lugar de nacimiento"
    },
    {
        "id": "nacionalidad",
        "grupo": "personal",
        "texto": "¿Cuál es tu *nacionalidad actual*?",
        "campo": "Nacionalidad"
    },
    {
        "id": "estado_civil",
        "grupo": "personal",
        "texto": "¿Cuál es tu *estado civil*?\n\n1 — Soltero/a\n2 — Casado/a\n3 — Unión libre\n4 — Divorciado/a\n5 — Viudo/a",
        "campo": "Estado civil"
    },

    # ══════════════════════════════════
    # GRUPO 2: PASAPORTE
    # ══════════════════════════════════
    {
        "id": "pasaporte_numero",
        "grupo": "pasaporte",
        "texto": "¿Cuál es el *número de tu pasaporte*?",
        "campo": "Número de pasaporte"
    },
    {
        "id": "pasaporte_emision",
        "grupo": "pasaporte",
        "texto": "¿Cuál es la *fecha de emisión* del pasaporte?\n\n_(día/mes/año)_",
        "campo": "Fecha de emisión del pasaporte"
    },
    {
        "id": "pasaporte_vencimiento",
        "grupo": "pasaporte",
        "texto": "¿Cuál es la *fecha de vencimiento* del pasaporte?\n\n_(Debe tener al menos 3 meses más allá del regreso)_",
        "campo": "Fecha de vencimiento del pasaporte"
    },
    {
        "id": "pasaporte_emitido_por",
        "grupo": "pasaporte",
        "texto": "¿En qué *ciudad fue emitido* el pasaporte?\n\n_(Ej: Guayaquil)_",
        "campo": "Ciudad de emisión del pasaporte"
    },

    # ══════════════════════════════════
    # GRUPO 3: EL VIAJE
    # ══════════════════════════════════
    {
        "id": "pais_destino",
        "grupo": "viaje",
        "texto": "¿Cuál es el *país principal* que vas a visitar en Europa?\n\n_(El consulado donde tramites debe ser del país donde más días pasas)_",
        "campo": "País principal de destino"
    },
    {
        "id": "otros_paises",
        "grupo": "viaje",
        "texto": "¿Vas a visitar *otros países de Europa* además del principal?\n\nSi sí, lista cuáles. Si no, escribe *No*",
        "campo": "Otros países a visitar"
    },
    {
        "id": "fecha_entrada",
        "grupo": "viaje",
        "texto": "¿Cuándo planeas *llegar a Europa*?\n\n_(día/mes/año)_",
        "campo": "Fecha de entrada"
    },
    {
        "id": "fecha_salida",
        "grupo": "viaje",
        "texto": "¿Cuándo planeas *regresar a Ecuador*?\n\n_(día/mes/año)_",
        "campo": "Fecha de salida"
    },
    {
        "id": "motivo_viaje",
        "grupo": "viaje",
        "texto": "¿Cuál es el *motivo principal del viaje*?\n\n1 — Turismo / vacaciones\n2 — Visita a familiar o amigo\n3 — Negocio / reunión\n4 — Evento (festival, deporte, etc.)\n5 — Otro (indica cuál)",
        "campo": "Motivo del viaje"
    },
    {
        "id": "alojamiento",
        "grupo": "viaje",
        "texto": "¿Dónde te vas a *hospedar* en Europa?\n\nIndica nombre del hotel o dirección de la persona que te recibe.",
        "campo": "Alojamiento en Europa"
    },
    {
        "id": "quien_paga",
        "grupo": "viaje",
        "texto": "¿Quién *financia el viaje*?\n\n1 — Yo mismo (efectivo, tarjeta, cuenta bancaria)\n2 — Mi empleador\n3 — Un familiar (indica quién)\n4 — Otra persona (indica quién)",
        "campo": "Quién financia el viaje"
    },

    # ══════════════════════════════════
    # GRUPO 4: CONTACTO EN ECUADOR
    # ══════════════════════════════════
    {
        "id": "direccion_ecuador",
        "grupo": "contacto",
        "texto": "¿Cuál es tu *dirección completa en Ecuador*?\n\n_(Calle, número, sector, ciudad)_",
        "campo": "Dirección en Ecuador"
    },
    {
        "id": "telefono",
        "grupo": "contacto",
        "texto": "¿Cuál es tu *número de celular* principal?",
        "campo": "Teléfono celular"
    },
    {
        "id": "email",
        "grupo": "contacto",
        "texto": "¿Cuál es tu *correo electrónico*?",
        "campo": "Correo electrónico"
    },

    # ══════════════════════════════════
    # GRUPO 5: TRABAJO Y FINANZAS
    # ══════════════════════════════════
    {
        "id": "ocupacion",
        "grupo": "trabajo",
        "texto": "¿Cuál es tu *ocupación actual*?\n\n_(Ej: Contador, Docente, Comerciante, Estudiante, Independiente)_",
        "campo": "Ocupación"
    },
    {
        "id": "empleador",
        "grupo": "trabajo",
        "texto": "¿Cuál es el *nombre y dirección de tu empleador* o institución educativa?\n\nSi eres independiente, indica tu actividad.",
        "campo": "Empleador / Institución"
    },
    {
        "id": "salario_mensual",
        "grupo": "trabajo",
        "texto": "¿Cuánto es tu *ingreso mensual aproximado* en dólares?",
        "campo": "Ingreso mensual (USD)"
    },
    {
        "id": "saldo_bancario",
        "grupo": "trabajo",
        "texto": "¿Cuánto tienes aproximadamente en tu *cuenta bancaria* ahora mismo?\n\n_(El Schengen pide mínimo $50-100 por día de estadía)_",
        "campo": "Saldo bancario aproximado (USD)"
    },
    {
        "id": "bienes",
        "grupo": "trabajo",
        "texto": "¿Tienes *propiedades o bienes* en Ecuador (casa, carro, terreno, negocio)?\n\nSi sí, lista cuáles. Si no, escribe *No*\n\n_(Estos vínculos con Ecuador fortalecen el expediente)_",
        "campo": "Bienes en Ecuador"
    },

    # ══════════════════════════════════
    # GRUPO 6: HISTORIAL DE VISAS
    # ══════════════════════════════════
    {
        "id": "visa_schengen_anterior",
        "grupo": "historial",
        "texto": "¿Alguna vez te *otorgaron una visa Schengen*?\n\nSi sí: ¿cuándo y para qué país? Si no, escribe *No*",
        "campo": "Visa Schengen anterior"
    },
    {
        "id": "rechazo_schengen",
        "grupo": "historial",
        "texto": "¿Alguna vez te *negaron una visa Schengen u otra visa europea*?\n\nSi sí: ¿cuándo y cuál fue la razón? Si no, escribe *No*",
        "campo": "Rechazo Schengen previo"
    },
    {
        "id": "huella_digital",
        "grupo": "historial",
        "texto": "¿Ya tienes tus *huellas digitales registradas* en el sistema Schengen (VIS)?\n\nSi viajaste a Europa antes, es probable que sí. Si no, escribe *No sé* o *No*",
        "campo": "Huellas digitales en VIS"
    },
    {
        "id": "viajes_previos",
        "grupo": "historial",
        "texto": "¿Has viajado a algún *país fuera de Ecuador* en los últimos 3 años?\n\nSi sí: lista los países y año aproximado. Si no, escribe *No*",
        "campo": "Viajes internacionales recientes"
    },
]
