import inspect
import pandas as pd
from datetime import datetime
import gspread
import os
import logging

from dotenv import load_dotenv
from .email_notifications import EmailNotification

email = EmailNotification()
logger = logging.getLogger(__name__)
load_dotenv()

class GoogleConnection():
    """
    Se settea la cuenta de servicio de google.
    """
    def __init__(self):
        self.gservice = self._authenticate()

    def _authenticate(self):
        key_path = os.getenv('GOOGLE_SHEETS_SERVICE_ACCOUNT')
        if not key_path:
            raise ValueError("Error: La variable de entorno 'GOOGLE_SHEETS_SERVICE_ACCOUNT' no está definida.")
        
        try:
            return gspread.service_account(filename=key_path)
        except gspread.exceptions.APIError as e:
            frame = inspect.currentframe()
            method_name = frame.f_code.co_name if frame else "Unknown"
            body = f"Error en la conexion a Google Sheets: {e}\nError en el metodo: {method_name}"
            error_message = "Error al autenticar la cuenta de servicio."
            email.sendFailedNotification(
                subject=error_message,
                body=body
            )
            logger.exception("Error de API de Google Sheets: %s", e)
            raise

class ReadGoogleSheet(GoogleConnection):
    """
    Agregar el libro y las hojas necesarias
    """
    def __init__(self, workbook: str, worksheet:str, headers: list):
        super().__init__()
        self.workbook = workbook
        self.worksheet = worksheet
        self.headers = headers
        self.today = str(datetime.today().strftime('%Y-%m-%d'))
        self.datetime = datetime.today().strftime("%d/%m/%Y %H:%M:%S")

    def getRecords(self) -> pd.DataFrame | None:
        try:
            wb = self.gservice.open(self.workbook)
            ws = wb.worksheet(self.worksheet)
            records = ws.get_all_records(expected_headers=self.headers, head=2)
            self.df = pd.DataFrame(records)
            return self.df
        except gspread.exceptions.APIError as e:
            frame = inspect.currentframe()
            method_name = frame.f_code.co_name if frame else "Unknown"
            body = f"Error al intentar obtener los datos de la tabla en Google Sheet: {e}\nError en el metodo: {method_name}"
            error_message = "Error: Conexion Google Sheets"
            email.sendFailedNotification(
                subject=error_message,
                body=body
            )
            logger.exception("Error de API de Google Sheets: %s", e)
