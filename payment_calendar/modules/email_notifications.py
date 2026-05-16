import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

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
            logger.error("Missing required environment variables (EMAIL, RECEIVER, PASSWORD)")
            exit()
                      
        if body == "":
            body = "Esta semana no se agregaron nuevas tareas."
        
        logger.info("Enviando notificacion...")

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
            logger.info(body)
            logger.info("Correo enviado con éxito.")
        except Exception as e:
            logger.exception("Error enviando el correo: %s", e)
            exit()

    
    def sendFailedNotification(self, subject:str, body:str) -> None:
        sender_email = os.getenv('EMAIL')
        receiver_email = os.getenv('RECEIVER')
        password = os.getenv('PASSWORD')            
        # subject = f"FAILED in the Google tasks process."
        
        if not sender_email or not receiver_email or not password:
            logger.error("Missing required environment variables (EMAIL, RECEIVER, PASSWORD)")
            exit()
        
        logger.warning("Algo salio mal. Enviando detalle por correo...")

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
            logger.info("Correo enviado con éxito.")
        except Exception as e:
            logger.exception("Error enviando el correo: %s", e)
            exit()
