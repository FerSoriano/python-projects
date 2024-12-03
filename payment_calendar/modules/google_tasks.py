from datetime import datetime
import os.path
import inspect

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .email_notifications import EmailNotification

SCOPES = ["https://www.googleapis.com/auth/tasks"]
email = EmailNotification()

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
                        email.sendFailedNotification(
                            f"Error al renovar el token: {refresh_error}. Solicitando nueva autorización."
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
            error_message = f"Error al autenticar: {e}"
            print(error_message)
            email.sendFailedNotification(error_message)
            raise

  def _request_new_credentials(self):
        """Solicitar nuevas credenciales al usuario"""
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                "./modules/credentials.json", SCOPES
            )
            return flow.run_local_server(port=0)
        except Exception as e:
            error_message = f"Error al solicitar nuevas credenciales: {e}"
            print(error_message)
            email.sendFailedNotification(error_message)
            raise

  def getTasksID(self, task_list_name:str) -> list:
    try:
      results = self.service.tasklists().list(maxResults=10).execute()
      items = results.get("items", [])
      task_list = []

      if not items:
        print("No task lists found.")
        return

      for item in items:
        task = {
          "task_name":item['title'],
          "task_id":item['id']
        }
        task_list.append(task)
      
      for task in task_list:
        if task['task_name'] == task_list_name:
          return task['task_id']
      
      print("List name not found.")
    except:
       method_name = inspect.currentframe().f_code.co_name # Obtener el nombre del método actual
       email.sendFailedNotification(f"Error obteniendo el TaskID. Error en el metodo: {method_name}")

  def getTasks(self, task_list_name: str) -> list:
    task_list_id = self.getTasksID(task_list_name)
    if not task_list_id:
        print("La lista no fue encontrada.")
        return

    try:
      results = self.service.tasks().list(tasklist=task_list_id).execute()
      tasks = results.get("items", [])

      if not tasks:
          print("No tasks found in the list.")
          return []

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
          print(f"Tarea: {task_title}, Estado: {task_status}, Fecha límite: {due_date_formatted}")
      return tasks
    
    except:
       method_name = inspect.currentframe().f_code.co_name # Obtener el nombre del método actual
       email.sendFailedNotification(f"Error obteniendo las tareas. Error en el metodo: {method_name}")
  
  def createTask(self, task_list_name: str, task_name: str, due_date: str, notes: str) -> tuple:
    """
    Returns (True, text) if the task is created successfully.
    """
    task_list_id = self.getTasksID(task_list_name)
    if not task_list_id:
        print("La lista no fue encontrada.")
        return
    
    results = self.service.tasks().list(tasklist=task_list_id).execute()
    tasks = results.get("items", [])
    
    try:
        due_date_iso = datetime.strptime(due_date, '%Y-%m-%d').isoformat() + 'Z'
    except ValueError:
        print("El formato de fecha debe ser YYYY-MM-DD.")
        method_name = inspect.currentframe().f_code.co_name # Obtener el nombre del método actual
        email.sendFailedNotification(f"Error en el metodo: {method_name}\nEl formato de fecha debe ser YYYY-MM-DD.")
        exit()
    
    new_task = {
        'title': task_name,
        'due': due_date_iso,
        'notes': notes
    }
    
    # print(self.tasks)
    for task in tasks:
        task_due = datetime.fromisoformat(task['due'].replace("Z", "")).isoformat() + 'Z' # normalizar la fecha sin milisegundos
        if (task['title'] == new_task['title']) and (task_due == new_task['due']):
           text = 'La tarea ya se encuentra registrada con la misma fecha.'
           return False, text

    try:
        self.service.tasks().insert(tasklist=task_list_id, body=new_task).execute()
        text = f"Tarea '{task_name}' creada con éxito para el dia: {due_date}"
        return True, text
    except HttpError as error:
        print(f"Ocurrió un error al crear la tarea: {error}")
        method_name = inspect.currentframe().f_code.co_name # Obtener el nombre del método actual
        email.sendFailedNotification(f"Ocurrió un error al crear la tarea: {error}\nError en el metodo: {method_name}")


if __name__ == "__main__":
  google = GoogleTaskManager()
  list_name = "Mis tareas"

