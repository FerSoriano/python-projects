from config import ExportImportData

WORKBOOK = 'Gestor-Notificaciones'
MAIN_WORKSHEET = 'inicio'
LOG_WORKSHEET = 'log'

libro = ExportImportData(workbook=WORKBOOK,main_worksheet=MAIN_WORKSHEET,log_worksheet=LOG_WORKSHEET)
libro.setConection()
libro.getRecords()
libro.setActiveRangeDate()

libro.sendNotification()
libro.updateWorksheet()
