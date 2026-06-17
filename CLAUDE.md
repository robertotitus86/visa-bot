# INSTRUCCIONES — visa-bot (WhatsApp Bot Asesoría Visa Global)

## QUÉ ES ESTE PROYECTO
Bot de WhatsApp para Asesoría Visa Global. Hecho en Python, desplegado en Render.
URL producción: https://visa-bot-seqw.onrender.com
WhatsApp de Roberto: +593 98 784 6751

## API CRÍTICA — ANTHROPIC EXCLUSIVO PARA ESTE BOT
La API de Anthropic (sk-ant-...) se usa EXCLUSIVAMENTE aquí.
NUNCA usarla para contenido, copy, imágenes ni nada fuera del bot.
Todo lo demás usa Gemini (gratuito).

## ARCHIVOS CLAVE

| Archivo | Función |
|---------|---------|
| `bot.py` | Entrada principal — webhook WhatsApp, routing de mensajes |
| `system_prompt.py` | Prompt del sistema para Claude — personalidad y reglas del bot |
| `onboarding_flow.py` | Flujo de bienvenida y calificación inicial del lead |
| `lead_qualifier.py` | Calificación automática de leads (puntaje, segmento) |
| `ds160_flow.py` + `ds160_preguntas.py` | Flujo guiado del DS-160 |
| `analisis_cliente.py` | Análisis del perfil del cliente para recomendaciones |
| `sheets_integration.py` | Integración con Google Sheets (CRM backend) |
| `crm_lookup.py` | Consultas al CRM desde el bot |
| `followup_manager.py` | Gestión de seguimientos automáticos |
| `recordatorios.py` | Recordatorios programados |
| `paypal_integration.py` | Integración de pagos PayPal |
| `schengen_flow.py` + `schengen_preguntas.py` | Flujo visa Schengen |
| `uk_flow.py` + `uk_preguntas.py` | Flujo visa Reino Unido |
| `render.yaml` | Configuración de deploy en Render |

## DEPLOY EN RENDER
- Plataforma: Render (render.com)
- Checklist de deploy: `RENDER_CHECKLIST.md`
- Variables de entorno en Render dashboard (no en código)
- Cada push a main → redeploy automático

## BUGS CRÍTICOS CONOCIDOS

### PayPhone — NUNCA agregar storeId — CRÍTICO
La función `payphonePrepare` en `appscript_portal.js` NO debe tener `storeId` en el body.
Enviarlo causa error 100 "La tienda no existe". Probado: sin storeId funciona perfecto.
El token correcto está en GAS Script Properties como `PAYPHONE_TOKEN`.
Links de PayPhone son de un solo uso — si el cliente lo abre dos veces da 404, eso es normal.

### Tag [CERRAR:] — truncar ANTES del tag, no hacer replace — CRÍTICO
El bot hace `bot_reply = bot_reply[:tag_full_start].strip()` para enviar solo el texto
que Claude escribió ANTES del tag. Si se usa `.replace()` se envía también el texto de después.
Claude ignora las reglas del system_prompt y escribe texto después del tag — el código lo filtra.

### Palabras híbridas inglés/español — filtro en código — NO TOCAR
`limpiar_palabras()` en `bot.py` reemplaza "resendo", "resendarlo", "includes" etc. antes de enviar.
El system_prompt solo no es suficiente — Claude Haiku las genera de todas formas.
NUNCA eliminar esta función ni el llamado `limpiar_palabras(reply)` en `_process_wa_ia`.

### JSON.parse de respuestas Claude — CRÍTICO
NUNCA hacer JSON.parse() directo sobre respuesta de Claude.
Siempre extraer con regex primero (Claude a veces envuelve en markdown):
```python
import re, json
match = re.search(r'\{[\s\S]*\}', text.replace('```json','').replace('```',''))
data = json.loads(match.group()) if match else {}
```

### Detección de menores — edad < 18 no < 14
Un "menor" en visa USA = cualquier persona menor de 18 años.
El código original usaba < 14, enviaba adolescentes 14-17 por flujo de adultos.

### mode: no-cors no devuelve respuesta
fetch() con mode: 'no-cors' tiene respuesta opaca — no se puede confirmar éxito.
Mostrar "guardado" con advertencia de que es tentativo.

## DOCUMENTOS DE REFERENCIA
- `REPORTE_AUDITORIA.md` — auditoría del bot
- `VALIDACION_INFORMACION_2026.md` — validación de datos 2026
- `COMPLIANCE_UPDATE_100.md` — actualizaciones de compliance
- `META_COMPLIANCE_GUIDE.md` — guía de cumplimiento Meta

## PRESUPUESTO
API Anthropic: monitorear uso — NUNCA gastar sin revisar límites primero.
Avisar a Roberto si se acerca al límite mensual.
