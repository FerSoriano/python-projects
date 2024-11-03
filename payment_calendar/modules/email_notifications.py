import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailNotification():
    def __init__(self):
        pass

    def sendNotification(self, body:str) -> None:
        sender_email = os.getenv('EMAIL')
        receiver_email = os.getenv('RECEIVER')
        password = os.getenv('PASSWORD')            
        subject = f"New payments added in Google tasks"
                      
        if body == "":
            body = "Esta semana no se agregaron nuevas tareas."
        
        print(f"Enviando notificacion...")

        #TODO: separar en otro metodo
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

    
    def sendFailedNotification(self, body:str) -> None:
        sender_email = os.getenv('EMAIL')
        receiver_email = os.getenv('RECEIVER')
        password = os.getenv('PASSWORD')            
        subject = f"FAILED in the Google tasks process."
        
        print(f"Error en la ejecucion. Enviando notificacion...")

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