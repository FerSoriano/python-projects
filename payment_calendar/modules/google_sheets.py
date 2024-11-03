import inspect
import pandas as pd
from datetime import datetime
import gspread

from dotenv import load_dotenv
from .email_notifications import EmailNotification

email = EmailNotification()
load_dotenv()

class GoogleConnection():
    """
    Se settea la cuenta de servicio de google.
    """
    def __init__(self) -> None:
        self.service_account = './key/key.json'

    def setConection(self):
        try:
            self.gc = gspread.service_account(filename=self.service_account)
        except gspread.exceptions.APIError as e:
            method_name = inspect.currentframe().f_code.co_name # Obtener el nombre del método actual
            email.sendFailedNotification(f"Error en la conexion a Google Sheets: {e}\nError en el metodo: {method_name}")
            print(f"Error de API de Google Sheets: {e}")


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

    def getRecords(self) -> pd.DataFrame:
        try:
            wb = self.gc.open(self.workbook)
            ws = wb.worksheet(self.worksheet)
            records = ws.get_all_records(expected_headers=self.headers, head=2)
            self.df = pd.DataFrame(records)
            return self.df
        except gspread.exceptions.APIError as e:
            method_name = inspect.currentframe().f_code.co_name # Obtener el nombre del método actual
            email.sendFailedNotification(f"Error al intentar obtener los datos de la tabla en Google Sheet: {e}\nError en el metodo: {method_name}")
            print(f"Error de API de Google Sheets: {e}")
