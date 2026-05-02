import os
import json
from datetime import datetime

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON", "")


def get_client():
    if not GSPREAD_AVAILABLE:
        raise RuntimeError("gspread no instalado")
    if not CREDENTIALS_JSON:
        raise RuntimeError("GOOGLE_CREDENTIALS_JSON no configurado")

    creds_dict = json.loads(CREDENTIALS_JSON)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return gspread.authorize(creds)


def guardar_en_sheets(personas: list, datos: list, tipo_visa: str, phone: str, analisis: list = None) -> bool:
    if not SPREADSHEET_ID or not CREDENTIALS_JSON:
        print("Sheets no configurado — omitiendo")
        return False

    try:
        gc = get_client()
        sh = gc.open_by_key(SPREADSHEET_ID)

        # Hoja según tipo de visa
        nombres_hoja = {
            "USA DS-160": "Clientes USA",
            "Schengen": "Clientes Schengen",
            "Reino Unido": "Clientes UK",
        }
        nombre_hoja = nombres_hoja.get(tipo_visa, "Clientes")

        try:
            ws = sh.worksheet(nombre_hoja)
        except gspread.WorksheetNotFound:
            ws = sh.add_worksheet(title=nombre_hoja, rows=1000, cols=60)

        # Si la hoja está vacía, agregar encabezados
        if ws.row_count == 0 or not ws.row_values(1):
            encabezados = ["Fecha", "Telefono", "Tipo Visa", "Nombre", "Analisis IA"]
            if datos:
                encabezados += list(datos[0].keys())
            ws.append_row(encabezados)

        # Agregar fila por cada persona
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        for i, nombre in enumerate(personas):
            datos_persona = datos[i] if i < len(datos) else {}
            analisis_texto = analisis[i] if analisis and i < len(analisis) else ""

            fila = [fecha, phone, tipo_visa, nombre, analisis_texto]
            fila += list(datos_persona.values())
            ws.append_row(fila)

        print(f"Sheets: {len(personas)} persona(s) guardadas en '{nombre_hoja}'")
        return True

    except Exception as e:
        print(f"Error guardando en Sheets: {e}")
        return False
