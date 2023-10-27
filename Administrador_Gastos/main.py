from class_file import AdminGastos
import clear_downloads as cd
from datetime import date

CONCEPTOS_DEBITO = {
            "Ingresos": ['abono/nomina', 'pago recibido', 'traspaso', 
                         'deposito en ventanilla', 'deposito por devolucion', 'disponible banamex'],
            "Gastos Fijos": ['pago de servicio', 'deposito inversion perfiles', 'microsoft', 'banco invex']
            }

CONCEPTOS_CREDITO = {
            "Streaming": ['disney','spotify','netflix'],
            "Amazon": ['amazon'],
            "Mercado Libre": ['merpago', 'mercado pago'],
            "TicketMaster": ['ticketmaster'],
            "Pago Tarjeta": ['su abono'],
            "QuickLearning": ['ql del'],
            "Prestamo Credito":['disponible citibanamex'],
            "Intereses":['interes', 'iva', 'comision ext']
            }

DOWNLOAD_FILE = '/Users/fersoriano/Downloads/Descargas_PDF'
PATH = '/Users/fersoriano/Documents/programming/python-projects-main/Administrador_Gastos/'
PDF_FOLDER = PATH + 'PDF/'
PDF_LOG_FOLDER = PDF_FOLDER + 'log/'
PDF_NAME = ['EstadodeCuenta.pdf','EstadodeCuenta_BSmart.pdf','EstadodeCuenta_Simplicity.pdf']
EXCEL_PATH = PATH + 'Excel/'
EXCEL_FILE = EXCEL_PATH + 'master.xlsx'
CSV_TEMPS = [EXCEL_PATH + 'records.csv', EXCEL_PATH + 'records_temp_1.csv', EXCEL_PATH + 'records_temp_2.csv']
YEAR = date.today().year

cd.clear_downloads()
cd.show_moved_files()

# TARJETA DEBITO
tarjeta_debito = AdminGastos(nombre_tarjeta='debito', sheet_name='records_debito',conceptos=CONCEPTOS_DEBITO
                             ,ruta=PATH,pdf_folder=PDF_FOLDER,download_file=DOWNLOAD_FILE,pdf_log_folder=PDF_LOG_FOLDER
                             ,pdf_name = PDF_NAME[0],pdf_path=PDF_FOLDER + PDF_NAME[0],excel_file=EXCEL_FILE
                             ,csv_temps=CSV_TEMPS,year=YEAR)
tarjeta_debito.move_pdf()
tarjeta_debito.extract_pdf_debito()
tarjeta_debito.update_excel()


# TARJETA B-SMART
tarjeta_bsmart = AdminGastos(nombre_tarjeta='bsmart', sheet_name='records_bsmart',conceptos=CONCEPTOS_CREDITO
                             ,ruta=PATH,pdf_folder=PDF_FOLDER,download_file=DOWNLOAD_FILE,pdf_log_folder=PDF_LOG_FOLDER
                             ,pdf_name=PDF_NAME[1],pdf_path=PDF_FOLDER + PDF_NAME[1],excel_file=EXCEL_FILE
                             ,csv_temps=CSV_TEMPS,year=YEAR)
tarjeta_bsmart.move_pdf()
tarjeta_bsmart.extract_pdf_credito()
tarjeta_bsmart.update_excel()


# TARJETA SIMPLICITY
tarjeta_simplicity = AdminGastos(nombre_tarjeta='simplicity',sheet_name='records_simplicity',conceptos=CONCEPTOS_CREDITO
                                 ,ruta=PATH,pdf_folder=PDF_FOLDER,download_file=DOWNLOAD_FILE,pdf_log_folder=PDF_LOG_FOLDER
                                 ,pdf_name=PDF_NAME[2],pdf_path=PDF_FOLDER + PDF_NAME[2],excel_file=EXCEL_FILE
                                 ,csv_temps=CSV_TEMPS,year=YEAR)
tarjeta_simplicity.move_pdf()
tarjeta_simplicity.extract_pdf_credito()
tarjeta_simplicity.update_excel()


