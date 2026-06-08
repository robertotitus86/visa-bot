import os
import requests
import json
from datetime import datetime

PAYPAL_CLIENT_ID     = os.getenv("PAYPAL_CLIENT_ID", "")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET", "")
PAYPAL_MODE          = os.getenv("PAYPAL_MODE", "live")  # "sandbox" para pruebas

BASE_URL = "https://api.paypal.com" if PAYPAL_MODE == "live" else "https://api.sandbox.paypal.com"

PAQUETES = {
    "ESENCIAL":     {"precio": 197, "nombre": "Paquete Esencial — Asesoría Visa Global"},
    "PROFESIONAL":  {"precio": 250, "nombre": "Paquete Profesional — Asesoría Visa Global"},
    "VIP":          {"precio": 320, "nombre": "Paquete VIP — Asesoría Visa Global"},
    "MEXICO":       {"precio": 79,  "nombre": "Asesoría Visa México — Visa Global"},
    "RENOVACION":   {"precio": 79,  "nombre": "Renovación Visa USA — Visa Global"},
    "REVISION":     {"precio": 49,  "nombre": "Revisión Exprés de Documentos — Visa Global"},
    "URGENTE_ESENCIAL":    {"precio": 247, "nombre": "Paquete Esencial Urgente — Visa Global"},
    "URGENTE_PROFESIONAL": {"precio": 300, "nombre": "Paquete Profesional Urgente — Visa Global"},
    "URGENTE_VIP":         {"precio": 370, "nombre": "Paquete VIP Urgente — Visa Global"},
}


def _get_access_token() -> str:
    resp = requests.post(
        f"{BASE_URL}/v1/oauth2/token",
        auth=(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET),
        data={"grant_type": "client_credentials"},
        headers={"Accept": "application/json"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def crear_orden(paquete: str, telefono_cliente: str) -> dict:
    """Crea una orden PayPal y devuelve {order_id, approval_url}."""
    pkg = PAQUETES.get(paquete.upper(), PAQUETES["PROFESIONAL"])
    token = _get_access_token()

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": str(pkg["precio"]),
            },
            "description": pkg["nombre"],
            "custom_id": telefono_cliente,
        }],
        "application_context": {
            "brand_name": "Asesoría Visa Global",
            "landing_page": "BILLING",
            "user_action": "PAY_NOW",
            "return_url": "https://www.asesoriadevisadosglobal.com/pago-exitoso.html",
            "cancel_url": "https://www.asesoriadevisadosglobal.com/pago-cancelado.html",
        },
    }

    resp = requests.post(
        f"{BASE_URL}/v2/checkout/orders",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    approval_url = next(
        (link["href"] for link in data.get("links", []) if link["rel"] == "approve"),
        None,
    )
    return {"order_id": data["id"], "approval_url": approval_url, "paquete": paquete, "precio": pkg["precio"]}


def verificar_pago(order_id: str) -> dict | None:
    """Captura y verifica el pago de una orden. Devuelve datos del pago o None."""
    try:
        token = _get_access_token()
        resp = requests.post(
            f"{BASE_URL}/v2/checkout/orders/{order_id}/capture",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            timeout=15,
        )
        data = resp.json()
        if data.get("status") == "COMPLETED":
            unit = data["purchase_units"][0]
            capture = unit["payments"]["captures"][0]
            return {
                "order_id": order_id,
                "telefono": unit.get("custom_id", ""),
                "monto": capture["amount"]["value"],
                "moneda": capture["amount"]["currency_code"],
                "payer_email": data.get("payer", {}).get("email_address", ""),
                "fecha": datetime.now().isoformat(),
                "status": "COMPLETED",
            }
    except Exception as e:
        print(f"Error verificando pago {order_id}: {e}")
    return None


def verificar_webhook_signature(headers: dict, body: bytes) -> bool:
    """Verifica que el webhook venga realmente de PayPal."""
    webhook_id = os.getenv("PAYPAL_WEBHOOK_ID", "")
    if not webhook_id:
        print("[PAYPAL] PAYPAL_WEBHOOK_ID no configurado — rechazando webhook por seguridad")
        return False
    try:
        token = _get_access_token()
        payload = {
            "transmission_id":   headers.get("paypal-transmission-id", ""),
            "transmission_time": headers.get("paypal-transmission-time", ""),
            "cert_url":          headers.get("paypal-cert-url", ""),
            "auth_algo":         headers.get("paypal-auth-algo", ""),
            "transmission_sig":  headers.get("paypal-transmission-sig", ""),
            "webhook_id":        webhook_id,
            "webhook_event":     json.loads(body),
        }
        resp = requests.post(
            f"{BASE_URL}/v1/notifications/verify-webhook-signature",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=payload,
            timeout=10,
        )
        return resp.json().get("verification_status") == "SUCCESS"
    except Exception as e:
        print(f"Error verificando webhook: {e}")
        return False
