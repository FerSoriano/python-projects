import datetime
from modules import GoogleTaskManager, ReadGoogleSheet, EmailNotification

WORKBOOK = 'Gastos Mensuales 2024'
WORKSHEET = 'Control Pagos'
HEADERS = ['Tipo', 'Concepto', 'Fecha', 'Fecha Pago', 'Semana', 'Monto', 'Comentarios', 'Pagado']
LIST_NAME = 'Mis tareas'

week_num = datetime.datetime.today().isocalendar()[1]

googleSheetData = ReadGoogleSheet(workbook=WORKBOOK,worksheet=WORKSHEET,headers=HEADERS)
googleTasks = GoogleTaskManager()
email = EmailNotification()

googleSheetData.setConection()
df = googleSheetData.getRecords()
try:
    df = df[(df['Tipo']=='Tarjetas') & (df['Semana']==week_num)]
except:
    email.sendFailedNotification("Error al obtener el Dataframe.")
    exit()

body = ""
for i,row in df.iterrows():
    task_name = f'Pagar {row['Concepto']}'
    due_date = row['Fecha Pago']
    notes = f'Total a pagar: {row['Monto']}'
    
    create_task = googleTasks.createTask(task_list_name=LIST_NAME, task_name=task_name, due_date=due_date, notes=notes)
    
    if create_task[0]:
        print(create_task[1])
        body += create_task[1]
        body += '\n'
    else:
        print(create_task[1])

email.sendNotification(body=body)