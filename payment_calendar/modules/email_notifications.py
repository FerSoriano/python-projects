import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailNotification():
    def __init__(self):
        pass

    def sendNotification(self, body: str, subject: str = "") -> None:
        sender_email = os.getenv('EMAIL')
        receiver_email = os.getenv('RECEIVER')
        password = os.getenv('PASSWORD')
        if not subject:            
            subject = f"New payments added in your Google Calendar"
        
        if not sender_email or not receiver_email or not password:
            print("Error: Missing required environment variables (EMAIL, RECEIVER, PASSWORD)")
            exit()
                      
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

    
    def sendFailedNotification(self, subject:str, body:str) -> None:
        sender_email = os.getenv('EMAIL')
        receiver_email = os.getenv('RECEIVER')
        password = os.getenv('PASSWORD')            
        # subject = f"FAILED in the Google tasks process."
        
        if not sender_email or not receiver_email or not password:
            print("Error: Missing required environment variables (EMAIL, RECEIVER, PASSWORD)")
            exit()
        
        print(f"Algo salio mal. Enviando detalle por correo...")

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