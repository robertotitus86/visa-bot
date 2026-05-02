import os
import json
import re
import requests
from datetime import datetime

WEBHOOK_URL = os.getenv("GOOGLE_SHEETS_WEBHOOK", "")


def _extraer_probabilidad(analisis: str) -> str:
    if not analisis:
        return ""
    match = re.search(r"PROBABILIDAD[^:]*:\s*(\d+%)", analisis, re.IGNORECASE)
    return match.group(1) if match else ""


def _extraer_paquete(analisis: str) -> str:
    if not analisis:
        return ""
    match = re.search(r"PAQUETE RECOMENDADO[^:]*:\s*([^\n]+)", analisis, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def guardar_en_sheets(personas: list, datos: list, tipo_visa: str,
                      phone: str, analisis: list = None) -> bool:
    if not WEBHOOK_URL:
        print("Sheets webhook no configurado — omitiendo")
        return False

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    ok_count = 0

    for i, nombre in enumerate(personas):
        campos = datos[i] if i < len(datos) else {}
        analisis_txt = analisis[i] if analisis and i < len(analisis) else ""

        probabilidad = _extraer_probabilidad(analisis_txt)
        paquete = _extraer_paquete(analisis_txt)

        # Encabezados fijos + campos del formulario
        encabezados_fijos = ["Fecha", "Telefono", "Tipo Visa", "Nombre",
                             "Probabilidad", "Paquete Recomendado", "Analisis IA"]
        encabezados = encabezados_fijos + list(campos.keys())

        fila_fija = [fecha, phone, tipo_visa, nombre,
                     probabilidad, paquete, analisis_txt]
        fila = fila_fija + list(campos.values())

        payload = {
            "tipo_visa":   tipo_visa,
            "encabezados": encabezados,
            "fila":        fila,
        }

        try:
            resp = requests.post(
                WEBHOOK_URL,
                json=payload,
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            result = resp.json()
            if result.get("status") == "ok":
                print(f"Sheets OK — {nombre} fila {result.get('fila')}")
                ok_count += 1
            else:
                print(f"Sheets error — {result.get('msg')}")
        except Exception as e:
            print(f"Sheets excepcion — {e}")

    return ok_count == len(personas)
