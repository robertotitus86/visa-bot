# CHECKLIST RENDER — Visa Global Bot

**Última actualización:** 16 junio 2026

## Variables de Entorno REQUERIDAS ✅

Todas estas deben estar en **Render Dashboard → Environment Variables**:

### CRÍTICAS (El bot NO funciona sin estas)
- [ ] `ANTHROPIC_API_KEY` = sk-ant-...
  - **Dónde obtenerla:** console.anthropic.com
  - **Qué hace:** Procesa respuestas de Claude
  
- [ ] `WA_TOKEN` = EAAcHS35...
  - **Dónde obtenerla:** Facebook Business → Configuración → Tokens permanentes
  - **Qué hace:** Envía mensajes de WhatsApp

- [ ] `GEMINI_API_KEY` = AIzaSy...
  - **Dónde obtenerla:** aistudio.google.com
  - **Qué hace:** Genera recordatorios y resúmenes diarios
  - **Sin ella:** Recordatorios no funcionan, pero el bot sigue respondiendo

- [ ] `RESEND_API_KEY` = re_...
  - **Dónde obtenerla:** resend.com → API keys
  - **Qué hace:** Envía emails de recordatorios

### IMPORTANTES (Seguridad — endpoints admin se bloquean sin estas)
- [ ] `FOLLOWUP_SECRET` = [contraseña aleatoria fuerte]
  - **Qué hace:** Protege endpoints `/send-recordatorios`, `/send-resumen`, `/test`, `/reset`
  - **Sin ella:** Endpoints admin no funcionan

- [ ] `ADMIN_PANEL_SECRET` = [contraseña aleatoria fuerte]
  - **Qué hace:** Protege panel /admin
  - **Sin ella:** Panel de admin no accesible

- [ ] `META_APP_SECRET` = [secret de Meta]
  - **Dónde obtenerla:** Facebook Business → Configuración → Secretos
  - **Qué hace:** Verifica webhook de WhatsApp (firma HMAC)
  - **Sin ella:** Webhook funciona pero sin verificación

### OPCIONALES (Telegram)
- [ ] `TELEGRAM_TOKEN` = [bot token de Telegram]
  - **Sin ella:** Endpoints de Telegram retornan error

## Variables de Configuración (Ya configuradas ✅)
- [x] `VERIFY_TOKEN` = visaglobal2026 (webhook WhatsApp)
- [x] `PHONE_NUMBER` = 593994442512 (número del bot)
- [x] `PHONE_NUMBER_ID` = 1132483959957091 (ID de WhatsApp Business)
- [x] `RENDER_URL` = https://visa-global-bot.onrender.com

## Cómo Verificar que Está OK

### 1. Check inmediato (logs de Render)
```
Esperado:
✅ Bot iniciando — claves de entorno validadas

Si ves ERROR:
❌ ERROR CRÍTICA: ANTHROPIC_API_KEY no está configurada
→ Agrega la clave en Render Dashboard
```

### 2. Test del bot (WhatsApp)
Envía mensaje al bot: +593 99 444 2512
- ✅ Bot responde en < 30 segundos = Variables OK
- ❌ No responde en 2 minutos = Problema con claves

### 3. Test recordatorios (endpoint manual)
```bash
curl -X GET "https://visa-global-bot.onrender.com/send-recordatorios" \
  -H "X-Admin-Secret: [FOLLOWUP_SECRET]"
```

Esperado: `{"status": "enviando", "destinatarios": ["Luis Seas", "Zoila Guaman", "Paul Fernando", "Jenny Enid", "Mileidy", "Paul Smith"]}`

## Flujos Críticos

### 1. Mensaje WhatsApp → Respuesta
```
Cliente envía: "Hola"
↓
Bot recibe en /webhook (POST)
↓
Valida WA_TOKEN ✅
↓ 
Llama get_ai_response() con ANTHROPIC_KEY ✅
↓
Envía respuesta con WA_TOKEN ✅
```

### 2. Recordatorio diario (9:00 AM Ecuador)
```
APScheduler dispara enviar_recordatorios()
↓
Valida GEMINI_KEY ✅ (genera consejo del día)
↓
Para cada familia:
  - Valida RESEND_API_KEY → envía email
  - Valida WA_TOKEN → envía WhatsApp
```

## Si Algo Falla

### Bot no responde (error 404)
1. Espera 5 minutos (deploy en progreso)
2. Chequea Render Dashboard → Logs
3. Si ves "ANTHROPIC_API_KEY no está configurada" → Agrégala

### Recordatorios no se envían
1. Chequea: ¿Está GEMINI_API_KEY en Render?
2. Chequea: ¿Está RESEND_API_KEY en Render?
3. Dispara manual: `curl -X GET ... -H "X-Admin-Secret: ..."`
4. Chequea logs de Render

### Webhook Meta no verifica firma
1. Si META_APP_SECRET está vacío: Funciona sin verificación (⚠️ menos seguro)
2. Para arreglarlo: Agrega META_APP_SECRET en Render

## Rotar Claves (Cuando sea necesario)

### ANTHROPIC_API_KEY
1. Ve a: console.anthropic.com
2. Create new API key
3. Copia la nueva clave
4. En Render Dashboard: Actualiza ANTHROPIC_API_KEY
5. Render redeploya automáticamente

### GEMINI_API_KEY
1. Ve a: aistudio.google.com
2. Copia la clave (solo hay una por proyecto)
3. En Render Dashboard: Actualiza GEMINI_API_KEY
4. Espera redeploy (3-5 minutos)

## Checklist Pre-Deployment

Antes de cualquier cambio en código:
- [ ] Todas las variables CRÍTICAS están en Render
- [ ] Bot responde a /ping en < 5 segundos
- [ ] Un mensaje de WhatsApp recibe respuesta < 30 segundos
- [ ] Logs de Render no muestran "ERROR CRÍTICA"

## Historial de Problemas

| Fecha | Problema | Causa | Solución |
|-------|----------|-------|----------|
| 16 jun | Bot no responde | GEMINI_API_KEY faltaba | Agregada en Render |
| 16 jun | Recordatorios no funcionan | Info de Jenny incorrecta | Actualizado recordatorios.py |

---

**Last verified:** 16 junio 2026 15:30 UTC-5
