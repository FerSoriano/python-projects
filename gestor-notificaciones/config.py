import inspect
import os
import json

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
from datetime import datetime
import gspread

from dotenv import load_dotenv
load_dotenv()

class GoogleConnection():
    """
    Se settea la cuenta de servicio de google.
    """
    def __init__(self) -> None:
        self.service_account = './key/key.json'

    def setConection(self):
        self.gc = gspread.service_account(filename=self.service_account)


class ExportImportData(GoogleConnection):
    """
    Agregar el libro y las hojas necesarias
    """
    def __init__(self, workbook, main_worksheet, log_worksheet):
        super().__init__()
        self.workbook = workbook
        self.main_worksheet = main_worksheet
        self.log_worksheet = log_worksheet
        self.today = str(datetime.today().strftime('%Y-%m-%d'))
        self.datetime = datetime.today().strftime("%d/%m/%Y %H:%M:%S")

    def getRecords(self) -> pd.DataFrame:
        try:
            self.wb = self.gc.open(self.workbook)
            self.ws = self.wb.worksheet(self.main_worksheet)
            self.records = self.ws.get_all_records()
            self.df = pd.DataFrame(self.records)
            return self.df
        except gspread.exceptions.APIError as e:
            method_name = inspect.currentframe().f_code.co_name # Obtener el nombre del método actual
            self.sendFailedNotification(method=method_name,error=e)
            print(f"Error de API de Google Sheets: {e}")

    def setActiveRangeDate(self) -> None:
        self.df['isActive'] = self.df.apply(lambda row : 1 if ( self.today >= row['Fecha Inicio'] ) and ( self.today <= row['Fecha Fin'] ) else 0, axis=1)

    def takeMedicine(self) -> bool:
        df_active = self.df[self.df['isActive'] == 1]
        if df_active.iloc[0]['Tomar Pastillas?'] == 1:
            return True

    def updateWorksheet(self) -> None:
        try:
            data = [self.df.columns.values.tolist()] + self.df.values.tolist()
            self.ws.update('A1', data)
            print('La tabla fue actualizada')
        except gspread.exceptions.APIError as e:
            method_name = inspect.currentframe().f_code.co_name # Obtener el nombre del método actual
            self.sendFailedNotification(method=method_name,error=e)
            print(f"Error de API de Google Sheets: {e}")

    def updateLog(self, flag: str) -> None:
        try:
            new_record = [self.today, flag, self.datetime]
            log = self.wb.worksheet(self.log_worksheet)
            records = log.get_all_values()
            records.append(new_record)
            log.update('A1', records)
            print('Log actualizado')
        except gspread.exceptions.APIError as e:
            method_name = inspect.currentframe().f_code.co_name # Obtener el nombre del método actual
            self.sendFailedNotification(method=method_name,error=e)
            print(f"Error de API de Google Sheets: {e}")

    def sendNotification(self) -> None:
        if self.takeMedicine():
            sender_email = os.getenv('EMAIL')
            receiver_email = os.getenv('RECEIVER')
            password = os.getenv('PASSWORD')
            body = ""
            with open('./flags.json','r') as f:
                values = json.load(f)
                body += f"Recordatorio medicamento:\n"
                body += f"Dia: {values['dia']} / 15\n"
                body += f"Pastilla: {values['numero_pastilla']} / 2\n\n"
                body += f"Enviado el {self.datetime}"
            
            subject = f"Notificación Medicamento {values['numero_pastilla']} / 2"

            print(f"Enviando notificacion {values['numero_pastilla']} / 2...")
            
            self.sendEmail(sender_email,receiver_email,password,subject,body)
                           
            values['dia'] += 1 if values['numero_pastilla'] == 2 else 0
            values['numero_pastilla'] = 2 if values['numero_pastilla'] == 1 else 1
            with open('./flags.json', 'w') as f:
                json.dump(values, f, indent=4)
            self.updateLog('1')

        else:
            values = {
                "dia":1,
                "numero_pastilla":1
            }
            with open('./flags.json', 'w') as f:
                json.dump(values, f, indent=4)
            print('Hoy no se toma medicamento')
            self.updateLog('0')
        
    def sendFailedNotification(self, method: str, error: str) -> None:
        sender_email = os.getenv('EMAIL')
        receiver_failed_email = os.getenv('RECEIVER_FAILED')
        password = os.getenv('PASSWORD')
        subject = "Ejecucion fallida - Gestor Notificacion."
        body = f"Fallo en el proceso. No se pudo ejecutar el metodo: {method}.\n\n{error}"
        print(body)

        self.sendEmail(sender_email,receiver_failed_email,password,subject,body)


    def sendEmail(self, sender_email: str, receiver_email: str, password: str, subject: str, body: str) -> None:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email

        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            # Conecta con el servidor SMTP de Gmail
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()  # Inicia la conexión segura
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
            print("Correo enviado con éxito.")
        except Exception as e:
            print(f"Error enviando el correo: {e}")
            exit()






