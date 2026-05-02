"""
Gestión de follow-ups automáticos.
Almacena mensajes programados en Google Sheets.
Google Apps Script los ejecuta cada 30 minutos.
"""
import os
import json
import requests
from datetime import datetime, timedelta

SHEETS_WEBHOOK = os.getenv("GOOGLE_SHEETS_WEBHOOK", "")
SS_ID = "19yHZ5HJH5eWyFXej8ffGBT2_sttXDZtvNaCoNEzjIOU"


def programar_followup(telefono: str, phone_number_id: str, tipo: str,
                        mensaje: str, delay_horas: float, contexto: dict = None):
    """Guarda un follow-up pendiente en Google Sheets para envío futuro."""
    fecha_envio = (datetime.now() + timedelta(hours=delay_horas)).isoformat()
    try:
        requests.post(
            SHEETS_WEBHOOK,
            json={
                "accion": "guardar_followup",
                "telefono": telefono,
                "phone_number_id": phone_number_id,
                "tipo": tipo,
                "mensaje": mensaje,
                "fecha_envio": fecha_envio,
                "estado": "PENDIENTE",
                "contexto": json.dumps(contexto or {}),
            },
            timeout=10,
        )
    except Exception as e:
        print(f"Error programando follow-up {tipo} para {telefono}: {e}")


def cancelar_followups_pendientes(telefono: str, tipo_prefijo: str = ""):
    """Cancela follow-ups pendientes de un teléfono (cuando ya pagó o ya no aplica)."""
    try:
        requests.post(
            SHEETS_WEBHOOK,
            json={
                "accion": "cancelar_followups",
                "telefono": telefono,
                "tipo_prefijo": tipo_prefijo,
            },
            timeout=10,
        )
    except Exception as e:
        print(f"Error cancelando follow-ups para {telefono}: {e}")


def marcar_formulario_completado(telefono: str):
    """Cancela recordatorios de formulario cuando el cliente ya lo completó."""
    cancelar_followups_pendientes(telefono, tipo_prefijo="recordatorio_formulario")
