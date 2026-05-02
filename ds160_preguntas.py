GRUPOS = [
    {
        "id": "personal",
        "emoji": "👤",
        "titulo": "Datos Personales",
        "intro": "Empecemos con tus datos personales. Son las preguntas más básicas, ¡en 2 minutos terminamos este bloque!"
    },
    {
        "id": "pasaporte",
        "emoji": "📘",
        "titulo": "Pasaporte",
        "intro": "Ahora necesito los datos de tu pasaporte. Tenlo a la mano."
    },
    {
        "id": "viaje",
        "emoji": "✈️",
        "titulo": "El Viaje",
        "intro": "Perfecto. Ahora me cuentas sobre el viaje a USA."
    },
    {
        "id": "contacto",
        "emoji": "🏠",
        "titulo": "Dirección y Contacto",
        "intro": "Casi a la mitad. Ahora tu información de contacto en Ecuador."
    },
    {
        "id": "familia",
        "emoji": "👨‍👩‍👧",
        "titulo": "Familia",
        "intro": "Bien. Ahora algunas preguntas sobre tu familia. Son pocas."
    },
    {
        "id": "trabajo",
        "emoji": "💼",
        "titulo": "Trabajo o Estudios",
        "intro": "Excelente. Cuéntame sobre tu situación laboral o de estudios."
    },
    {
        "id": "historial",
        "emoji": "🗺️",
        "titulo": "Historial de Viajes",
        "intro": "Ya casi terminamos. Necesito saber si has viajado antes o tenido visas."
    },
    {
        "id": "seguridad",
        "emoji": "🔒",
        "titulo": "Preguntas Finales",
        "intro": "Último bloque. Son preguntas de seguridad que pide el formulario. La mayoría son No — responde honestamente."
    },
]

PREGUNTAS = [
    # ══════════════════════════════════
    # GRUPO 1: DATOS PERSONALES
    # ══════════════════════════════════
    {
        "id": "apellidos",
        "grupo": "personal",
        "texto": "¿Cuáles son tus *apellidos* tal como aparecen en el pasaporte?\n\n_(Ej: García Rodríguez)_",
        "campo": "Apellidos (como en pasaporte)"
    },
    {
        "id": "nombres",
        "grupo": "personal",
        "texto": "¿Y tus *nombres* completos como están en el pasaporte?\n\n_(Ej: María Elena)_",
        "campo": "Nombres (como en pasaporte)"
    },
    {
        "id": "otros_nombres",
        "grupo": "personal",
        "texto": "¿Has usado algún *otro nombre* oficialmente? (apellido de soltera, nombre de matrimonio, apodo legal)\n\nSi no, escribe *No*",
        "campo": "Otros nombres usados"
    },
    {
        "id": "fecha_nacimiento",
        "grupo": "personal",
        "texto": "¿Cuál es tu *fecha de nacimiento*?\n\n_(Formato: día/mes/año — Ej: 15/03/1988)_",
        "campo": "Fecha de nacimiento"
    },
    {
        "id": "ciudad_nacimiento",
        "grupo": "personal",
        "texto": "¿En qué *ciudad y país naciste*?\n\n_(Ej: Guayaquil, Ecuador)_",
        "campo": "Ciudad y país de nacimiento"
    },
    {
        "id": "nacionalidad",
        "grupo": "personal",
        "texto": "¿Cuál es tu *nacionalidad*?\n\n_(Ej: Ecuatoriana)_",
        "campo": "Nacionalidad"
    },
    {
        "id": "otra_nacionalidad",
        "grupo": "personal",
        "texto": "¿Tienes alguna *otra ciudadanía o nacionalidad* además de la ecuatoriana?\n\nSi no, escribe *No*",
        "campo": "Otra nacionalidad"
    },
    {
        "id": "cedula",
        "grupo": "personal",
        "texto": "¿Cuál es tu número de *cédula de identidad*?",
        "campo": "Número de cédula"
    },
    {
        "id": "genero",
        "grupo": "personal",
        "texto": "¿Cuál es tu *sexo*?\n\nEscribe *M* (Masculino) o *F* (Femenino)",
        "campo": "Sexo"
    },
    {
        "id": "estado_civil",
        "grupo": "personal",
        "texto": "¿Cuál es tu *estado civil*?\n\n1 — Soltero/a\n2 — Casado/a\n3 — Unión libre\n4 — Divorciado/a\n5 — Viudo/a\n6 — Separado/a",
        "campo": "Estado civil"
    },

    # ══════════════════════════════════
    # GRUPO 2: PASAPORTE
    # ══════════════════════════════════
    {
        "id": "pasaporte_numero",
        "grupo": "pasaporte",
        "texto": "¿Cuál es el *número de tu pasaporte*? (está en la primera página)",
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
        "texto": "¿Cuál es la *fecha de vencimiento* del pasaporte?\n\n_(día/mes/año)_",
        "campo": "Fecha de vencimiento del pasaporte"
    },
    {
        "id": "pasaporte_ciudad_emision",
        "grupo": "pasaporte",
        "texto": "¿En qué *ciudad* fue emitido el pasaporte?\n\n_(Ej: Guayaquil)_",
        "campo": "Ciudad de emisión del pasaporte"
    },
    {
        "id": "pasaporte_perdido",
        "grupo": "pasaporte",
        "texto": "¿Alguna vez *perdiste* un pasaporte o te lo *robaron*?\n\nSi sí, indica el número y año aproximado. Si no, escribe *No*",
        "campo": "Pasaporte perdido o robado"
    },

    # ══════════════════════════════════
    # GRUPO 3: EL VIAJE
    # ══════════════════════════════════
    {
        "id": "fecha_llegada",
        "grupo": "viaje",
        "texto": "¿Cuándo *planeas llegar a USA* aproximadamente?\n\n_(Ej: 20/07/2026)_",
        "campo": "Fecha de llegada a USA"
    },
    {
        "id": "dias_estadia",
        "grupo": "viaje",
        "texto": "¿Cuántos *días* piensas quedarte en USA?",
        "campo": "Días de estadía en USA"
    },
    {
        "id": "direccion_usa",
        "grupo": "viaje",
        "texto": "¿Cuál es la *dirección donde te vas a quedar* en USA?\n\n_(Hotel o casa de familiar/amigo — calle, ciudad, estado)_",
        "campo": "Dirección en USA"
    },
    {
        "id": "contacto_usa",
        "grupo": "viaje",
        "texto": "¿Cuál es el *nombre y teléfono de tu contacto en USA*?\n_(La persona del hotel, amigo o familiar donde te quedas)_",
        "campo": "Contacto en USA (nombre y teléfono)"
    },
    {
        "id": "quien_paga",
        "grupo": "viaje",
        "texto": "¿Quién *paga el viaje*?\n\n1 — Yo mismo\n2 — Mi empleador\n3 — Un familiar (indica quién)\n4 — Otra persona (indica quién)",
        "campo": "Quién paga el viaje"
    },
    {
        "id": "fondos_disponibles",
        "grupo": "viaje",
        "texto": "¿Cuánto dinero aproximado tienes *disponible para el viaje*?\n\n_(En dólares — esto sirve para el expediente)_",
        "campo": "Fondos disponibles para el viaje"
    },

    # ══════════════════════════════════
    # GRUPO 4: DIRECCIÓN Y CONTACTO
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
        "id": "redes_sociales",
        "grupo": "contacto",
        "texto": "El DS-160 pide tus *redes sociales* de los últimos 5 años.\n\n¿Cuáles usas y cuál es tu usuario en cada una?\n_(Facebook, Instagram, TikTok, Twitter/X, LinkedIn, etc.)_\n\nSi no tienes ninguna, escribe *Ninguna*",
        "campo": "Redes sociales (plataforma y usuario)"
    },

    # ══════════════════════════════════
    # GRUPO 5: FAMILIA
    # ══════════════════════════════════
    {
        "id": "padre_nombre",
        "grupo": "familia",
        "texto": "¿Cuál es el *nombre completo de tu padre*?\n\nSi es fallecido o no lo conoces, indícalo.",
        "campo": "Nombre completo del padre"
    },
    {
        "id": "padre_nacimiento",
        "grupo": "familia",
        "texto": "¿Cuál es la *fecha de nacimiento de tu padre*?\n\n_(Si no la sabes exacta, año aproximado está bien)_",
        "campo": "Fecha de nacimiento del padre"
    },
    {
        "id": "padre_en_usa",
        "grupo": "familia",
        "texto": "¿Tu padre está actualmente en *Estados Unidos*?\n\n*Sí* o *No*",
        "campo": "¿Padre en USA?"
    },
    {
        "id": "madre_nombre",
        "grupo": "familia",
        "texto": "¿Cuál es el *nombre completo de tu madre*?",
        "campo": "Nombre completo de la madre"
    },
    {
        "id": "madre_nacimiento",
        "grupo": "familia",
        "texto": "¿Cuál es la *fecha de nacimiento de tu madre*?",
        "campo": "Fecha de nacimiento de la madre"
    },
    {
        "id": "madre_en_usa",
        "grupo": "familia",
        "texto": "¿Tu madre está actualmente en *Estados Unidos*?\n\n*Sí* o *No*",
        "campo": "¿Madre en USA?"
    },
    {
        "id": "familiares_usa",
        "grupo": "familia",
        "texto": "¿Tienes algún otro *familiar en Estados Unidos* (hermanos, tíos, primos, abuelos)?\n\nSi sí, indica nombre y parentesco. Si no, escribe *No*",
        "campo": "Otros familiares en USA"
    },
    {
        "id": "pareja_datos",
        "grupo": "familia",
        "texto": "Si estás *casado/a o en unión libre*, necesito los datos de tu pareja:\n• Nombre completo\n• Fecha de nacimiento\n• Nacionalidad\n• Ciudad y país donde vive actualmente\n\nSi eres soltero/a, escribe *Soltero*",
        "campo": "Datos de la pareja (si aplica)"
    },

    # ══════════════════════════════════
    # GRUPO 6: TRABAJO O ESTUDIOS
    # ══════════════════════════════════
    {
        "id": "ocupacion",
        "grupo": "trabajo",
        "texto": "¿Cuál es tu *ocupación o trabajo actual*?\n\n_(Ej: Contador, Docente, Comerciante, Estudiante universitario, Independiente)_",
        "campo": "Ocupación actual"
    },
    {
        "id": "empleador_nombre",
        "grupo": "trabajo",
        "texto": "¿Cuál es el *nombre de la empresa o institución* donde trabajas o estudias?",
        "campo": "Empresa / Institución"
    },
    {
        "id": "empleador_direccion",
        "grupo": "trabajo",
        "texto": "¿Cuál es la *dirección de esa empresa o institución*?\n\n_(Calle, ciudad)_",
        "campo": "Dirección del empleador"
    },
    {
        "id": "empleador_telefono",
        "grupo": "trabajo",
        "texto": "¿Cuál es el *teléfono de tu trabajo o institución*?",
        "campo": "Teléfono del empleador"
    },
    {
        "id": "salario",
        "grupo": "trabajo",
        "texto": "¿Cuánto es tu *ingreso mensual* aproximado en dólares?\n\n_(Si eres estudiante y no tienes ingresos propios, escribe 0 e indica quién te sostiene)_",
        "campo": "Ingreso mensual (USD)"
    },
    {
        "id": "tiempo_trabajo",
        "grupo": "trabajo",
        "texto": "¿Cuánto tiempo llevas trabajando o estudiando ahí?\n\n_(Ej: 3 años, desde marzo 2022)_",
        "campo": "Tiempo en el trabajo/institución"
    },
    {
        "id": "trabajo_anterior",
        "grupo": "trabajo",
        "texto": "En los *últimos 5 años*, ¿tuviste algún trabajo anterior?\n\nSi sí: nombre empresa, cargo, ciudad, fechas (desde/hasta). Si no, escribe *No*",
        "campo": "Trabajo anterior (últimos 5 años)"
    },
    {
        "id": "educacion",
        "grupo": "trabajo",
        "texto": "¿Cuál es tu *nivel de educación más alto* completado?\n\n1 — Primaria\n2 — Secundaria / Bachillerato\n3 — Técnico / Tecnológico\n4 — Universidad (indica carrera y año de graduación)\n5 — Postgrado / Maestría / Doctorado",
        "campo": "Nivel de educación"
    },

    # ══════════════════════════════════
    # GRUPO 7: HISTORIAL DE VIAJES
    # ══════════════════════════════════
    {
        "id": "viajes_previos_usa",
        "grupo": "historial",
        "texto": "¿Has estado alguna vez en *Estados Unidos*?\n\nSi sí: ¿cuándo fue la última vez y por cuánto tiempo? Si no, escribe *No*",
        "campo": "Visitas previas a USA"
    },
    {
        "id": "visa_usa_anterior",
        "grupo": "historial",
        "texto": "¿Alguna vez te *otorgaron una visa USA*?\n\nSi sí: número de visa y fecha de emisión. Si no, escribe *No*",
        "campo": "Visa USA anterior"
    },
    {
        "id": "rechazo_usa",
        "grupo": "historial",
        "texto": "¿Alguna vez te *negaron una visa USA* o te cancelaron un permiso de entrada?\n\nSi sí: ¿cuándo y cuál fue la razón? Si no, escribe *No*",
        "campo": "Rechazo visa USA"
    },
    {
        "id": "rechazo_otros_paises",
        "grupo": "historial",
        "texto": "¿Alguna vez te negaron una visa de *otro país* (Europa, Canadá, Reino Unido, etc.)?\n\nSi sí: ¿cuál país y cuándo? Si no, escribe *No*",
        "campo": "Rechazo visa otros países"
    },
    {
        "id": "viajes_internacionales",
        "grupo": "historial",
        "texto": "¿Has viajado a algún *país fuera de Ecuador* en los últimos 5 años?\n\nSi sí: lista los países y año aproximado. Si no, escribe *No*",
        "campo": "Viajes internacionales previos"
    },
    {
        "id": "peticion_inmigrante",
        "grupo": "historial",
        "texto": "¿Alguien en USA ha iniciado algún trámite de *residencia o inmigración* a tu nombre?\n\n*Sí* o *No*",
        "campo": "Petición de inmigrante en USA"
    },

    # ══════════════════════════════════
    # GRUPO 8: SEGURIDAD
    # ══════════════════════════════════
    {
        "id": "seg_enfermedad",
        "grupo": "seguridad",
        "texto": "¿Tienes o has tenido alguna *enfermedad contagiosa* (tuberculosis, lepra, etc.)?\n\n*Sí* o *No*",
        "campo": "Enfermedad contagiosa"
    },
    {
        "id": "seg_drogas",
        "grupo": "seguridad",
        "texto": "¿Has consumido *drogas ilegales* o tienes dependencia a alguna sustancia?\n\n*Sí* o *No*",
        "campo": "Consumo de drogas"
    },
    {
        "id": "seg_arrestado",
        "grupo": "seguridad",
        "texto": "¿Alguna vez has sido *arrestado, detenido o condenado* por algún delito en cualquier país?\n\nSi sí: indica el delito, país y año. Si no, escribe *No*",
        "campo": "Antecedentes penales"
    },
    {
        "id": "seg_deportado",
        "grupo": "seguridad",
        "texto": "¿Alguna vez fuiste *deportado o removido* de algún país?\n\n*Sí* o *No*",
        "campo": "Deportación previa"
    },
    {
        "id": "seg_terrorismo",
        "grupo": "seguridad",
        "texto": "¿Has estado involucrado en alguna *actividad terrorista, genocidio o persecución política*?\n\n*No* si nunca has tenido nada que ver con eso.",
        "campo": "Terrorismo / Actividad ilegal"
    },
]
