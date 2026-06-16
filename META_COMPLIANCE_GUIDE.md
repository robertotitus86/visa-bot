# META COMPLIANCE + CLARIDAD DE VENTA
**Documento crítico para no perder ventas ni incumplir normas de Meta**

---

## I. NORMAS META QUE PODRÍAS ESTAR INCUMPLIENDO

### ❌ RIESGO 1: Falta claridad sobre lo gratis vs pagado
**Meta Rule:** Usuarios deben saber exactamente qué es gratis y qué es de pago.

**Tu situación actual:**
- Dices "te hago una evaluación gratis"
- Pero el cliente NO sabe si la evaluación que está recibiendo AHORA es esa, o si viene después
- Cliente piensa: "Primero me responde gratis, luego me cobra la evaluación completa"
- Cliente se siente engañado cuando le cierres venta → RECLAMO META

**Solución:** Ser explícito desde el primer mensaje:
```
"Te voy a hacer una evaluación rápida y GRATIS ahora mismo en el chat 
— solo responde 4 preguntas y te doy el análisis real, sin costo."
```

### ❌ RIESGO 2: No explicas qué incluye la consulta gratis
**Meta Rule:** El usuario debe saber exactamente qué obtiene gratis.

**Tu situación actual:**
- Haces 4 preguntas
- Das un diagnóstico
- Cierras venta
- Pero el cliente siente que "SOLO" recibió 4 preguntas

**Solución:** Después del diagnóstico, dile explícitamente:
```
"Ya hiciste tu consulta gratis — revisé tu caso, te di análisis real, 
te mostré tus fortalezas y puntos de atención.

Eso que acabas de recibir es lo que otros asesores cobran $50–100 USD. 

Lo que viene ahora es opcional: 
- Si quieres solo estos datos → Ya tienes, es tuyo
- Si quieres que te arme la estrategia y te acompañe hasta la aprobación → Eso es el paquete"
```

### ⚠️ RIESGO 3: No diferencias claramente entre diagnóstico gratis y estrategia pagada

**Línea clave a agregar en ETAPA 3:**
```
"El diagnóstico que acabas de recibir es GRATIS y te pertenece.
Esto es lo que crees que vale ~ $50–100 USD en otras asesorías.

La diferencia con el Paquete Profesional $197 es que:
— GRATIS: sabes cuáles son tus puntos débiles
— PROFESIONAL: armamos la estrategia exacta, te preparamos para la entrevista
               y estamos contigo hasta que apruebes"
```

---

## II. CAMBIOS ESPECÍFICOS AL BOT

### CAMBIO 1: Primer mensaje (GANCHO DE ENTRADA)
**Buscar en system_prompt.py línea ~985**

**Reemplazar:**
```
"Te puedo hacer una evaluación rápida y gratis de tu caso..."
```

**Por:**
```
"Te voy a hacer una evaluación rápida y GRATIS AHORA MISMO en el chat 
— sin costo, sin compromiso. Solo necesito que respondas 4 preguntas 
para darte un análisis real de tu situación."
```

**Por qué:** El cliente sabe AHORA que la consulta es AHORA. No espera "después".

---

### CAMBIO 2: Después de Pregunta 4 (ANTES del diagnóstico)
**Buscar en system_prompt.py línea ~1020**

**Agregar ANTES de dar el diagnóstico:**
```
"Perfecto [nombre], ya tengo la información que necesito. 
Aquí va tu evaluación real — esto es lo que la mayoría de asesores cobran $50 USD:"
```

**Por qué:** Valida el trabajo que acabas de hacer. El cliente sabe que eso tiene valor.

---

### CAMBIO 3: Al dar el diagnóstico (ETAPA 3)
**Buscar en system_prompt.py línea ~1035–1060**

**Agregar ANTES de ofrecer el paquete:**
```
"[Aquí va el diagnóstico]

Ahora — lo que acabas de leer es tu consulta GRATIS completa. 
Ya sabes exactamente dónde estás y qué ve el consulado.

Si prefieres solo esto → listo, es tuyo.

Si quieres que vaya más allá y te arme la estrategia completa 
para blindar esos puntos débiles y acompañarte hasta la aprobación,
eso es el Paquete Profesional: $197."
```

**Por qué:** Claridad absoluta. El cliente SABE qué recibió gratis y qué cuesta.

---

### CAMBIO 4: En PROTOCOLO DE NO PERDER VENTA (NIVEL 3)
**Buscar línea ~1146**

**Agregar antes de ofrecer descuento:**
```
"Entiendo que la venta es mucho dinero. Déjame ser claro:

Ya recibiste tu evaluación gratis — eso está hecho.
Esto que te ofrezco ahora ($177 en lugar de $197) es solo la estrategia 
y acompañamiento si decides continuar.

¿Hacemos el profesional a $177?"
```

**Por qué:** El cliente sabe que YA TIENE VALOR gratis. Lo que rechaza es el acompañamiento, no la consulta.

---

## III. CUMPLIMIENTO META

### ✅ Lo que estás haciendo bien:
- Opt-out con "STOP" funciona
- No enviás spam (respondes a iniciativa del cliente)
- Tienes números claros (no falsas promesas)
- Tienes política de garantía (si te niegan, revisamos sin costo)

### ⚠️ Lo que necesitas arreglar:
1. **Ser explícito que la consulta gratis es AHORA** (no después)
2. **Mostrar el valor de lo que da gratis** (para que no parezca demasiado poco)
3. **Diferenciar diagnóstico de estrategia** (uno es gratis, otra es de pago)
4. **No hacer parecer engaño** (tipo "te doy algo gratis para engancharte")

---

## IV. DEFENSA CONTRA RECLAMOS META

Si alguien dice "No sabía que era de pago" o "Me engañó el bot":

**Pruebas que tienes:**
1. Primer mensaje dice "GRATIS"
2. Diagnóstico es entregado antes de cerrar venta
3. Paquete se ofrece DESPUÉS del diagnóstico (no antes)
4. Cliente rechazó pero SIGUE teniendo su diagnóstico (no se lo quitaste)
5. Garantía: si te rechaza después de pagar, revisamos gratis

---

## V. CHECKLIST PRE-DEPOY

- [ ] Primer mensaje claramente dice "evaluación GRATIS AHORA MISMO"
- [ ] Después de diagnóstico, aclara "esto que recibiste es GRATIS"
- [ ] Paquete se ofrece SIEMPRE después del diagnóstico, no antes
- [ ] Si rechaza, deja claro que MANTIENE su diagnóstico gratis
- [ ] No hay promesas falsas ("garantizo aprobación")
- [ ] Opt-out STOP funciona
- [ ] Los $37 del diagnóstico solo se ofrecen si rechaza paquete

---

## VI. EJEMPLO COMPLETO DEL FLUJO CORRECTO

```
Bot (1er mensaje):
"Te voy a hacer una evaluación rápida y GRATIS ahora mismo en el chat."

Cliente responde 4 preguntas...

Bot (después de P4):
"Perfecto, esto es tu análisis real — lo que otros cobran $50 USD:"

Bot (diagnóstico):
[da diagnóstico]

"Eso que acabas de leer es tu consulta GRATIS.
Si quieres la estrategia + acompañamiento, es el Profesional $197."

Cliente dice: "Es mucho dinero, no puedo"

Bot:
"Entiendo. Ya tienes tu diagnóstico (eso es tuyo para siempre).
¿Quieres al menos el análisis escrito? Son $37 — es el máximo descuento."

Cliente rechaza todo

Bot:
"Sin problema [nombre]. Tu diagnóstico ya está listo — úsalo como base.
Si cambias de idea, aquí estaré.
¿Te dejo en el radar para dar seguimiento?"
```

---

## VII. META COMPLIANCE CHECKLIST

- [x] No es spam (responde a iniciativa)
- [x] Claros los costos (no hay sorpresas)
- [x] Usuario puede opt-out (STOP funciona)
- [ ] **Diferencia clara gratis/pagado** ← FIX THIS
- [ ] No hace promesas falsas (no "garantizo aprobación")
- [x] Información honesta (datos de mercado verificables)
- [ ] **Cliente mantiene valor gratis aunque rechace** ← FIX THIS

---

**Última revisión:** 16 junio 2026
**Status:** 🔴 REQUIERE ACTUALIZACIÓN EN SYSTEM_PROMPT.PY
