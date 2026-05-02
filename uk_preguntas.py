GRUPOS_UK = [
    {
        "id": "personal",
        "emoji": "👤",
        "titulo": "Datos Personales",
        "intro": "Empecemos con tus datos personales para la visa del Reino Unido."
    },
    {
        "id": "pasaporte",
        "emoji": "📘",
        "titulo": "Pasaporte",
        "intro": "Datos de tu pasaporte. El UK pide que tenga al menos 6 meses de validez."
    },
    {
        "id": "viaje",
        "emoji": "✈️",
        "titulo": "El Viaje al Reino Unido",
        "intro": "Detalles del viaje. El consulado quiere saber exactamente qué vas a hacer."
    },
    {
        "id": "contacto",
        "emoji": "🏠",
        "titulo": "Contacto y Alojamiento",
        "intro": "Tu dirección en Ecuador y dónde te quedarás en UK."
    },
    {
        "id": "finanzas",
        "emoji": "💰",
        "titulo": "Situación Financiera",
        "intro": "El Reino Unido es muy estricto con esto. Fondos sólidos son clave."
    },
    {
        "id": "trabajo",
        "emoji": "💼",
        "titulo": "Trabajo y Vínculos con Ecuador",
        "intro": "Necesitan ver que tienes razones sólidas para volver."
    },
    {
        "id": "historial",
        "emoji": "🗺️",
        "titulo": "Historial de Viajes y Visas",
        "intro": "Historial previo — viajes anteriores fortalecen mucho el caso para UK."
    },
]

PREGUNTAS_UK = [
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
        "texto": "¿En qué *ciudad y país naciste*?",
        "campo": "Lugar de nacimiento"
    },
    {
        "id": "nacionalidad",
        "grupo": "personal",
        "texto": "¿Cuál es tu *nacionalidad*?",
        "campo": "Nacionalidad"
    },
    {
        "id": "estado_civil",
        "grupo": "personal",
        "texto": "¿Cuál es tu *estado civil*?\n\n1 — Soltero/a\n2 — Casado/a\n3 — Unión libre\n4 — Divorciado/a\n5 — Viudo/a",
        "campo": "Estado civil"
    },
    {
        "id": "hijos",
        "grupo": "personal",
        "texto": "¿Tienes *hijos*? Si sí, indica cuántos y sus edades.\n\nSi no, escribe *No*\n\n_(Los hijos en Ecuador son un vínculo fuerte para el caso)_",
        "campo": "Hijos (cantidad y edades)"
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
        "texto": "¿Cuál es la *fecha de vencimiento* del pasaporte?\n\n_(Debe tener al menos 6 meses de validez después del regreso)_",
        "campo": "Fecha de vencimiento del pasaporte"
    },
    {
        "id": "pasaporte_anterior",
        "grupo": "pasaporte",
        "texto": "¿Tienes algún *pasaporte anterior*?\n\nSi sí: número y fecha de vencimiento. Si no, escribe *No*\n\n_(Los pasaportes anteriores con sellos de viajes fortalecen el caso)_",
        "campo": "Pasaporte anterior"
    },

    # ══════════════════════════════════
    # GRUPO 3: EL VIAJE
    # ══════════════════════════════════
    {
        "id": "fecha_llegada",
        "grupo": "viaje",
        "texto": "¿Cuándo planeas *llegar al Reino Unido*?\n\n_(día/mes/año)_",
        "campo": "Fecha de llegada a UK"
    },
    {
        "id": "fecha_salida",
        "grupo": "viaje",
        "texto": "¿Cuándo planeas *regresar a Ecuador*?\n\n_(día/mes/año)_",
        "campo": "Fecha de salida de UK"
    },
    {
        "id": "motivo_viaje",
        "grupo": "viaje",
        "texto": "¿Cuál es el *motivo principal del viaje* al Reino Unido?\n\n1 — Turismo (museos, ciudades, cultura)\n2 — Visita a familiar o amigo\n3 — Evento específico (indica cuál)\n4 — Negocios / reunión\n5 — Otro (indica cuál)\n\n_(El UK quiere un propósito muy claro y detallado)_",
        "campo": "Motivo del viaje"
    },
    {
        "id": "ciudades_uk",
        "grupo": "viaje",
        "texto": "¿Qué *ciudades o lugares del Reino Unido* planeas visitar?\n\n_(Ej: Londres, Edimburgo, Liverpool — mientras más detallado, mejor)_",
        "campo": "Ciudades a visitar en UK"
    },
    {
        "id": "actividades",
        "grupo": "viaje",
        "texto": "¿Qué *actividades específicas* planeas hacer?\n\n_(Ej: visitar el Museo Británico, ver un partido de fútbol, recorrer Escocia, etc.)_",
        "campo": "Actividades planeadas"
    },

    # ══════════════════════════════════
    # GRUPO 4: CONTACTO Y ALOJAMIENTO
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
    {
        "id": "alojamiento_uk",
        "grupo": "contacto",
        "texto": "¿Dónde te vas a *hospedar en el Reino Unido*?\n\nIndica nombre del hotel y ciudad, o nombre y dirección de la persona que te recibe.",
        "campo": "Alojamiento en UK"
    },
    {
        "id": "contacto_uk",
        "grupo": "contacto",
        "texto": "Si tienes un *contacto en el Reino Unido* (familiar, amigo, conocido):\nIndica nombre completo, dirección y teléfono.\n\nSi no tienes ningún contacto allá, escribe *No tengo*",
        "campo": "Contacto en UK"
    },

    # ══════════════════════════════════
    # GRUPO 5: SITUACIÓN FINANCIERA
    # ══════════════════════════════════
    {
        "id": "saldo_bancario",
        "grupo": "finanzas",
        "texto": "¿Cuánto tienes aproximadamente en tu *cuenta bancaria* ahora mismo?\n\n_(El UK recomienda mínimo $5,000 para una estadía de 2 semanas — entre más, mejor)_",
        "campo": "Saldo bancario (USD)"
    },
    {
        "id": "tiempo_saldo",
        "grupo": "finanzas",
        "texto": "¿Hace cuánto tiempo tienes ese saldo en la cuenta aproximadamente?\n\n_(El UK revisa que el dinero no sea un depósito repentino — quieren ver estabilidad)_",
        "campo": "Antigüedad del saldo"
    },
    {
        "id": "presupuesto_viaje",
        "grupo": "finanzas",
        "texto": "¿Cuánto dinero aproximado tienes *presupuestado para el viaje* en total?\n\n_(Incluye vuelos, hotel, gastos diarios)_",
        "campo": "Presupuesto total del viaje (USD)"
    },
    {
        "id": "quien_financia",
        "grupo": "finanzas",
        "texto": "¿Quién *financia el viaje*?\n\n1 — Yo mismo\n2 — Mi empleador\n3 — Un familiar (indica quién y parentesco)\n4 — Otra persona (indica quién)",
        "campo": "Quién financia"
    },

    # ══════════════════════════════════
    # GRUPO 6: TRABAJO Y VÍNCULOS
    # ══════════════════════════════════
    {
        "id": "ocupacion",
        "grupo": "trabajo",
        "texto": "¿Cuál es tu *ocupación actual*?\n\n_(Ej: Gerente de ventas, Médico, Docente, Empresario, Estudiante)_",
        "campo": "Ocupación"
    },
    {
        "id": "empleador",
        "grupo": "trabajo",
        "texto": "¿Cuál es el *nombre y dirección de tu empleador* o negocio propio?\n\nSi eres estudiante, indica la institución.",
        "campo": "Empleador"
    },
    {
        "id": "salario",
        "grupo": "trabajo",
        "texto": "¿Cuánto es tu *ingreso mensual* aproximado en dólares?",
        "campo": "Ingreso mensual (USD)"
    },
    {
        "id": "tiempo_empleo",
        "grupo": "trabajo",
        "texto": "¿Cuánto tiempo llevas en tu trabajo o negocio actual?\n\n_(El UK valora estabilidad laboral — más tiempo = más fuerte el caso)_",
        "campo": "Tiempo en el empleo actual"
    },
    {
        "id": "bienes_ecuador",
        "grupo": "trabajo",
        "texto": "¿Tienes *propiedades o bienes* en Ecuador?\n\n_(Casa, carro, terreno, negocio, inversiones — todo suma como vínculo con Ecuador)_\n\nSi no tienes, escribe *No*",
        "campo": "Bienes en Ecuador"
    },
    {
        "id": "familia_ecuador",
        "grupo": "trabajo",
        "texto": "¿Tienes *familia directa en Ecuador* que depende de ti o con quien vives?\n\n_(Cónyuge, hijos, padres a cargo — son vínculos fuertes para demostrar que regresarás)_",
        "campo": "Familia en Ecuador"
    },

    # ══════════════════════════════════
    # GRUPO 7: HISTORIAL
    # ══════════════════════════════════
    {
        "id": "visa_uk_anterior",
        "grupo": "historial",
        "texto": "¿Alguna vez te *otorgaron una visa del Reino Unido*?\n\nSi sí: número de visa y fecha. Si no, escribe *No*",
        "campo": "Visa UK anterior"
    },
    {
        "id": "rechazo_uk",
        "grupo": "historial",
        "texto": "¿Alguna vez te *negaron una visa del Reino Unido*?\n\nSi sí: ¿cuándo y cuál fue la razón indicada? Si no, escribe *No*",
        "campo": "Rechazo visa UK"
    },
    {
        "id": "visa_usa_schengen",
        "grupo": "historial",
        "texto": "¿Tienes o tuviste visa *USA o Schengen* (Europa)?\n\nSi sí: indica cuál, vigente o vencida. Si no, escribe *No*\n\n_(Una visa USA o Schengen previa fortalece mucho el caso para UK)_",
        "campo": "Visa USA o Schengen previa"
    },
    {
        "id": "viajes_previos",
        "grupo": "historial",
        "texto": "¿Has viajado a algún *país fuera de Ecuador* en los últimos 5 años?\n\nSi sí: lista países y año aproximado. Si no, escribe *No*",
        "campo": "Viajes internacionales previos"
    },
    {
        "id": "rechazo_otros",
        "grupo": "historial",
        "texto": "¿Alguna vez te *negaron una visa de otro país* (USA, Schengen, Canadá, etc.)?\n\nSi sí: indica cuál y cuándo. Si no, escribe *No*",
        "campo": "Rechazo visa otros países"
    },
]
