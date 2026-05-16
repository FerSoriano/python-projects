from datetime import datetime
import os.path
import inspect
import logging
from typing import Optional, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .email_notifications import EmailNotification


SCOPES = ["https://www.googleapis.com/auth/tasks"]
email = EmailNotification()
logger = logging.getLogger(__name__)


class GoogleTaskManager():
  def __init__(self):
    self.service = self._authenticate()


  def _authenticate(self):
        creds = None
        try:
            # Intentar cargar credenciales desde un archivo
            if os.path.exists("./modules/token.json"):
                creds = Credentials.from_authorized_user_file("./modules/token.json", SCOPES)

            # Si no son válidas, intentar refrescar o solicitar nuevas credenciales
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                    except Exception as refresh_error:
                        body = f"Error al renovar el token: {refresh_error}. Solicitando nueva autorización."
                        email.sendFailedNotification(
                            subject="Payment Calendar: FAILED in the Google tasks process.",
                            body=body
                        )
                        creds = self._request_new_credentials()
                else:
                    creds = self._request_new_credentials()

                # Guardar el nuevo token
                with open("./modules/token.json", "w") as token:
                    token.write(creds.to_json())

            # Construir el servicio
            return build("tasks", "v1", credentials=creds)

        except Exception as e:
            body = f"Error al autenticar: {e}"
            logger.exception(body)
            email.sendFailedNotification(
                subject="Payment Calendar: FAILED in the Google tasks process.",
                body=body
            )
            raise


  def _request_new_credentials(self):
        """Solicitar nuevas credenciales al usuario"""
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                "./modules/credentials.json", SCOPES
            )
            # return flow.run_local_server(port=0)
            return flow.run_local_server(
                port=0,
                access_type="offline",
                prompt="consent"
            )
        except Exception as e:
            body = f"Error al solicitar nuevas credenciales: {e}"
            logger.exception(body)
            email.sendFailedNotification(
                subject="Payment Calendar: FAILED in the Google tasks process.",
                body=body
            )
            raise


  def getTasksID(self, task_list_name:str) -> Optional[str]:
    try:
        results = self.service.tasklists().list(maxResults=20).execute()
        items: list[dict[str, Any]] = results.get("items", [])

        if not items:
            logger.warning("No se encontraron listas de 'Tasks' activas.")
            return None

        for item in items:
            if item.get('title') == task_list_name:
                return item.get('id')
      
        logger.warning("La lista '%s' no fue encontrada.", task_list_name)
        return None
    except Exception as e:
        # Obtener el nombre del método actual
        frame = inspect.currentframe()
        method_name = frame.f_code.co_name if frame else "Unknown"
        body = f"Error obteniendo el TaskID. Error en el metodo: {method_name}. Error: {str(e)}"
        logger.exception(body)
        email.sendFailedNotification(
            subject="Payment Calendar: FAILED in the Google tasks process.",
            body=body
        )


  def getTasks(self, task_list_name: str) -> list:
    task_list_id = self.getTasksID(task_list_name)
    if not task_list_id:
        logger.warning("La lista no fue encontrada.")
        return []

    try:
      results = self.service.tasks().list(tasklist=task_list_id).execute()
      tasks = results.get("items", [])

      if not tasks:
          logger.info("No tasks found in the list.")
          return tasks

      for task in tasks:
          task_title = task.get('title')
          task_status = task.get('status')
          
          # Obtener y formatear la fecha límite, si está disponible
          due_date = task.get('due')
          if due_date:
              due_date = datetime.fromisoformat(due_date.replace("Z", ""))
              due_date_formatted = due_date.strftime('%Y-%m-%d')
          else:
              due_date_formatted = "No deadline"
          logger.info(
              "Tarea: %s, Estado: %s, Fecha límite: %s",
              task_title,
              task_status,
              due_date_formatted,
          )
      return tasks
    
    except Exception as e:
        frame = inspect.currentframe()
        method_name = frame.f_code.co_name if frame else "Unknown"
        body = f"Error obteniendo las tareas. Error en el metodo: {method_name}. Error: {e}"
        logger.exception(body)
        email.sendFailedNotification(
            subject="Payment Calendar: FAILED in the Google tasks process.",
            body=body
        )
        return []

  def createTask(self, task_list_name: str, task_name: str, due_date: str, notes: str) -> tuple:
    """
    Returns (True, text) if the task is created successfully.
    """
    task_list_id = self.getTasksID(task_list_name)
    if not task_list_id:
        msg = "La lista no fue encontrada."
        return False, msg
    
    results = self.service.tasks().list(tasklist=task_list_id).execute()
    tasks = results.get("items", [])
    
    try:
        due_date_iso = datetime.strptime(due_date, '%Y-%m-%d').isoformat() + 'Z'
    except ValueError:
        logger.error("El formato de fecha debe ser YYYY-MM-DD.")
        frame = inspect.currentframe()
        method_name = frame.f_code.co_name if frame else "Unknown"
        body = f"Error en el metodo: {method_name}\nEl formato de fecha debe ser YYYY-MM-DD."
        logger.exception(body)
        email.sendFailedNotification(
            subject="Payment Calendar: FAILED in the Google tasks process.",
            body=body
        )
        raise
    
    new_task = {
        'title': task_name,
        'due': due_date_iso,
        'notes': notes
    }
    
    for task in tasks:
        task_due = datetime.fromisoformat(task['due'].replace("Z", "")).isoformat() + 'Z' # normalizar la fecha sin milisegundos
        if (task['title'] == new_task['title']) and (task_due == new_task['due']):
           msg = 'La tarea ya se encuentra registrada con la misma fecha.'
           return False, msg

    try:
        self.service.tasks().insert(tasklist=task_list_id, body=new_task).execute()
        msg = f"Tarea '{task_name}' creada con éxito para el dia: {due_date}"
        return True, msg
    except HttpError as error:
        frame = inspect.currentframe()
        method_name = frame.f_code.co_name if frame else "Unknown"
        body = f"Ocurrió un error al crear la tarea: {error}\nError en el metodo: {method_name}"
        logger.exception(body)
        email.sendFailedNotification(
            subject="Payment Calendar: FAILED in the Google tasks process.",
            body=body
        )
        return False, body


if __name__ == "__main__":
  google = GoogleTaskManager()
  list_name = "Mis tareas"
