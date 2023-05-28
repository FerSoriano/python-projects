import shutil
import datetime as dt
from pathlib import Path
import PyPDF2
import tabula
import clear_downloads as cd
import pandas as pd
import numpy as np
import os

#TODO: Agregar las instancias para las tarjetas de credito.
#TODO: Gestionar los errores con mensajes personalizados. ie: Error al cargar. El libro se encuentra abierto.

class AdminGastos():
    def __init__(self, nombre_tarjeta, sheet_name, conceptos = dict, ruta = '', pdf_folder = '', download_file = '', pdf_log_folder = '',
                 pdf_name = '', pdf_path = '', excel_file = '', csv_temps = '') -> None:

        self.conceptos = conceptos
        self.nombre_tarjera = nombre_tarjeta
        self.sheet_name = sheet_name
        self.ruta = ruta
        self.pdf_folder = pdf_folder
        self.download_file = Path(download_file)
        self.pdf_log_folder = pdf_log_folder
        self.pdf_name = pdf_name
        self.pdf_path = pdf_path
        self.excel_file = excel_file
        self.csv_temps = csv_temps
        self.last_month = (dt.date.today().replace(day=1) - dt.timedelta(days=1))

        if ruta == '':
            self.ruta = 'D:\Proyectos\python-projects\Administrador_Gastos\\'

        if pdf_folder == '':
            self.pdf_folder = Path(f'{self.ruta}PDF\\')
        else:
            self.pdf_folder = Path(f'{self.ruta}{pdf_folder}')
        
        if download_file == '':
            self.download_file = Path('C:/Users/fer8f/Downloads/Descargas_PDF')

        if pdf_log_folder == '':
            self.pdf_log_folder = f'{self.ruta}PDF\log\\'

        if pdf_name == '': # file_name
            self.pdf_name = 'EstadodeCuenta.pdf'

        if pdf_path == '':
            self.pdf_path = f'{self.ruta}PDF\\' + self.pdf_name

        if excel_file == '':
            self.excel_file = f'{self.ruta}Excel\\master.xlsx'

        if csv_temps == '':
            self.csv_temps = [f'{self.ruta}Excel\\records.csv',f'{self.ruta}Excel\\records_temp_1.csv',f'{self.ruta}Excel\\records_temp_2.csv']


    def move_pdf(self):
        for file in self.pdf_folder.iterdir():
            if file.name == self.pdf_name:
                pdf_name_date = f'{file.stem} {self.last_month.strftime("%Y%m")}01{file.suffix}'
                shutil.move(file, self.pdf_log_folder + pdf_name_date)

        for file in self.download_file.iterdir():
            if file.name == self.pdf_name:
                shutil.move(file, self.pdf_path)
                print('Se movio el Estado de Cuenta.')

    def extract_pdf(self):
        pages = []
        pages_text = ''
        pdf_reader = PyPDF2.PdfFileReader(open(self.pdf_path, 'rb'))

        # extrae solo las paginas que tienen datos.
        valid = False
        while (valid == False):
            for i in range(1,(pdf_reader.getNumPages())):
                list_temp = tabula.read_pdf(self.pdf_path,pages=i,encoding='latin1')
                if list_temp == []:
                    if valid == True:
                        break
                else:
                    print('Agregando datos...')
                    pages.append(list_temp)
                    valid = True
        # elimina la primera hoja que es la info de la cuenta.
        pages.pop(0)    

        for page in range(0,len(pages)):
            pages_text = pages[page][0]
            df = pd.DataFrame(pages_text)

        # Validacion para cuando la primer fila 'SALDO ANTERIOR' no tenga fecha. Esto provoca que las lineas se desfacen.
            if page == 0:
                if pd.isna(df.loc[0, 'FECHA']):
                    df.loc[0, 'FECHA'] = '01 ENE'

            df2 = df[df.columns[0:2]] # fecha, concepto
            df2[df.columns[0]].replace('', np.nan, inplace=True) # fecha
    
            df3 = df[df.columns[-3:]] # retiros, depositos, saldo 
            df3[df.columns[-1:]].replace('', np.nan, inplace=True) # saldo
            
            if page == 0:
                df2.to_csv(self.csv_temps[1],index=False)
                df3.to_csv(self.csv_temps[2],index=False)
            else:
                df2.to_csv(self.csv_temps[1],mode='a',index=False,header=False) # agrega al csv sin encabezados.
                df3.to_csv(self.csv_temps[2],mode='a',index=False,header=False) # agrega al csv sin encabezados.
            
        df2 = pd.read_csv(self.csv_temps[1])
        df2.dropna(subset=[df.columns[0]], inplace=True)
        df2.reset_index(drop=True, inplace=True) 
        
        df3 = pd.read_csv(self.csv_temps[2]) 
        df3.dropna(subset=df.columns[-1:], inplace=True)  
        df3.reset_index(drop=True, inplace=True)

        result = pd.concat([df2, df3], axis=1, join="inner")

        result[result.columns[-2]].replace('', np.nan, inplace=True) # depositos
        result[result.columns[-3]].replace('', np.nan, inplace=True) # retiros
        result.dropna(subset=result.columns[-3:-1], how='all', inplace=True) # depositos, retiros

        # Se agrega la columna Sub Categoria.
        def asignar_subclasificacion(concepto):
            for clave, valores in self.conceptos.items():
                for valor in valores:
                    if valor in concepto.lower():
                        return clave
            return 'Gastos Variables'

        result['Sub Clasificacion'] = result['CONCEPTO'].apply(asignar_subclasificacion)   

        # Se agrega la columna Clasificacion.
        result['Clasificacion'] = result['Sub Clasificacion'].apply(lambda clas: 'Ingresos' if clas == 'Ingresos' else 'Egresos') 

        cols = ['Clasificacion', 'Sub Clasificacion', 'FECHA', 'CONCEPTO', 'RETIROS', 'DEPOSITOS', 'SALDO']
        result = result.reindex(columns=cols)

        # Se cambia el tipo de dato a numerico.
        try:
            result[['RETIROS', 'DEPOSITOS', 'SALDO']] = result[['RETIROS', 'DEPOSITOS', 'SALDO']].apply(lambda x: x.str.replace(',',''))
            result[['RETIROS', 'DEPOSITOS', 'SALDO']] = result[['RETIROS', 'DEPOSITOS', 'SALDO']].apply(pd.to_numeric)
        except:
            try:
                result[['RETIROS', 'DEPOSITOS', 'SALDO']] = result[['RETIROS', 'DEPOSITOS', 'SALDO']].apply(pd.to_numeric)
            except:
                print('ERROR. No se pudo cambiar los saldos a numericos.')  
                pass

        result.to_csv(self.csv_temps[0],index=False)

        # Borrar csv's temp
        for e in self.csv_temps[1:]:
            if os.path.isfile(e):
                os.remove(e)
                print(f'{e} --> Archivo temp eliminado.')
            
        
        # print(pages)
        print('Extact and Clear CSV Done!')


    def add_update_excel(self):
        df = pd.read_csv(self.csv_temps[0])
        sheet_name = 'records_' + self.sheet_name
        with pd.ExcelWriter(self.excel_file,mode="a",engine="openpyxl", if_sheet_exists='overlay') as writer:
            rows = writer.sheets[sheet_name].max_row
            df.to_excel(writer, sheet_name=sheet_name, header=None, startrow=rows, index=False)

        print("\nSe agrego la informacion al Master.")





conceptos = {
            "Ingresos": ['abono/nomina', 'pago recibido', 'traspaso', 
                         'deposito en ventanilla', 'deposito por devolucion', 'disponible banamex'],
            "Gastos Fijos": ['pago de servicio', 'deposito inversion perfiles', 'microsoft', 'banco invex']
            }

# cd.clear_downloads()
tarjeta_debito = AdminGastos(nombre_tarjeta='debito', sheet_name='test',conceptos=conceptos)
# tarjeta_debito.move_pdf()
tarjeta_debito.extract_pdf()
tarjeta_debito.add_update_excel()

