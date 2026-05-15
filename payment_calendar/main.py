import datetime
from modules import GoogleTaskManager, ReadGoogleSheet, EmailNotification, GoogleCalendarManager
import json


WORKBOOK = 'Gastos Mensuales'
WORKSHEET = 'Control Pagos'
HEADERS = ['Tipo', 'Concepto', 'Fecha', 'Fecha Pago', 'Semana', 'Monto', 'Comentarios', 'Pagado']
LIST_NAME = 'Mis tareas'
PAYMENT_TYPES = ['Tarjetas', 'Carro', 'Estudios', 'Mantenimiento']


with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)


def main():
    week_num = datetime.datetime.today().isocalendar()[1]

    google_sheet_data = ReadGoogleSheet(workbook=WORKBOOK,worksheet=WORKSHEET,headers=HEADERS)
    email = EmailNotification()

    google_tasks = None
    google_calendar = None

    if config['create_task']:
        google_tasks = GoogleTaskManager()

    if config['create_event']:
        google_calendar = GoogleCalendarManager()

    df = google_sheet_data.getRecords()

    if df is None:
        email.sendNotification(
            subject="Payment Calendar: Dataframe vacio",
            body="No pudo obtener informacion de Google Sheets."
        )
        return 

    body = ""
    
    try:
        df = df[(df['Tipo'].isin(PAYMENT_TYPES)) & (df['Semana']==week_num)]
    except:
        email.sendFailedNotification(
            subject="Payment Calendar: ERROR",
            body="Error al obtener el Dataframe."
        )
        return 

    for i,row in df.iterrows():
        task_name = f'Pagar {row['Concepto']}'
        due_date = row['Fecha Pago']
        notes = f'Total a pagar: {row['Monto']}'
        
        if google_tasks is not None:
            create_task = google_tasks.createTask(
                task_list_name=LIST_NAME, 
                task_name=task_name, 
                due_date=due_date, 
                notes=notes
            )
        
            if create_task[0]:
                print(create_task[1])
                body += create_task[1]
                body += '\n'
            else:
                print(create_task[1])
        

        if google_calendar is not None:
            create_event = google_calendar.add_event(
                event_name=task_name,
                due_date=due_date,
                notes=notes
            )

            if create_event[0]:
                body += create_event[1]
                body += '\n'
                
    email.sendNotification(body=body)

    return


if __name__ == "__main__":
    main()