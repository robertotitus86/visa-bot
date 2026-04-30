# Visa Global Bot

Bot de WhatsApp con IA para Asesoría Visa Global.

## Deploy en Render.com (gratis)

1. Sube esta carpeta a GitHub
2. Conecta en render.com con tu cuenta de GitHub
3. New Web Service → selecciona el repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn bot:app --host 0.0.0.0 --port $PORT`
6. Agrega variables de entorno desde render.yaml

## Webhook URL (para Meta WhatsApp)
```
https://tu-app.onrender.com/webhook
```

## Token de verificacion
```
visaglobal2026
```

## Test local
```
pip install -r requirements.txt
uvicorn bot:app --reload
```
