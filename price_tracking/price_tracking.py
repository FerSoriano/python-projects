"""
Scrip to get and track prices (Amazon / Mercado libre wishlist) week over week.
The data is stored in a private Google SpreadSheet.
You will be able to see the behaivor of each item.
"""

import config
import gspread
import time
from datetime import date
import statistics

class GoogleConnection():
    def __init__(self, service_account, workbook, worksheet):
        self.service_account = service_account
        self.workbook = workbook
        self.worksheet = worksheet
        self.start = time.time()

    def setConnection(self):
        self.gc = gspread.service_account(self.service_account)
    
    def getRecords(self):
        self.wb = self.gc.open(self.workbook)
        self.ws = self.wb.worksheet(self.worksheet)
        self.records = self.ws.get_all_records()
        self.records_list = self.ws.get_all_values()        
    
    def updateWorksheet(self):
        today = str(date.today())
        new_prices = [price for price in self.new_prices_zero]
        avg_list = [avg for avg in self.avg_list]
        comments = [comment for comment in self.comments]

        max_cols = len(self.records_list[0])
        max_rows = len(self.records_list)

        # set headers
        self.ws.update_cell(1 ,max_cols - 1, today)
        self.ws.update_cell(1 ,max_cols, 'AVG')
        self.ws.update_cell(1 ,max_cols + 1, 'Comments')

        # update cells
        for row in range(2, max_rows + 1):
            self.ws.update_cell(row ,max_cols - 1, new_prices[row - 2])
            self.ws.update_cell(row ,max_cols, avg_list[row - 2])
            self.ws.update_cell(row ,max_cols + 1, comments[row - 2])

        print('Se actualizaron los precios correctamente en Google Sheets. 📝')
        self.end = time.time()
        print(f'Tiempo total de ejecucion: {round((self.end - self.start),2)} seg.')


class PriceTracking(GoogleConnection):
    def __init__(self, service_account, workbook, worksheet):
        super().__init__(service_account, workbook, worksheet)
        self.elements = {     
            'xpath':'//*[@id="price"]/div/div[1]/div[1]/span/span/span[2]',
            'xpath_descuento':'//*[@id="price"]/div/div[1]/div[1]/span[1]/span/span[2]',
            'xpath_opcion':'//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[3]/div[1]/div[1]/span/span/span[2]',
            'xpath_opcion_descuento':'//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[3]/div[1]/div[1]/span[1]/span/span[2]'
            }
    
    def getPrices(self) -> None: # selenium
        self.prices = []
        def find_price(driver, element) -> str:
            price_element = driver.find_element(by='xpath', value=element)
            price = price_element.text
            time.sleep(2)
            driver.close()
            print(f'Precio: ${price}\n')
            return price
        
        def execute_selenium(self, url, element: dict, opcion = 'False'):
            time.sleep(1)
            driver = config.get_selenium_driver()
            driver.get(url)
            time.sleep(1)
            if opcion == 'False':
                try:
                    price = find_price(driver=driver,element=element['xpath'])
                    self.prices.append(price)
                except:
                    try:
                        price = find_price(driver=driver,element=element['xpath_descuento'])
                        self.prices.append(price)
                    except:
                        print('Ocurrio un error. No se encontro el precio. ❌')
                        driver.close()
                        self.prices.append('')
            else: #TODO: Revisar porque falla el codigo cuando el URL empieza por mercadolibre.com
                try:
                    price = find_price(driver=driver,element=element['xpath_opcion'])
                    self.prices.append(price)
                except:
                    try:
                        price = find_price(driver=driver,element=element['xpath_opcion_descuento'])
                        self.prices.append(price)
                    except:
                        print('Ocurrio un error. No se encontro el precio. ❌')
                        driver.close()
                        self.prices.append('')
        for e in self.records:
            print(f'Obteniendo informacion del articulo: {e["Articulo"]}...')
            execute_selenium(self, url=e['URL'], element=self.elements, opcion=e['Opcion'])
        if len(self.prices) < 1:
            print('No se pudo obtener ningun precio. Algo salio mal. ⚠️')
            exit()
        else:
            print('Se extrajeron los precios de los articulos. ✅')
            
    def transformPrices(self) -> None:
        self.avg_list = [] 
        self.comments = []
        
        # Se convierte a numero los precios 
        def converted_prices(self, prices_list):
            self.new_prices = []
            for price in prices_list:
                if price == '':
                    self.new_prices.append(price)
                else:
                    price = price.replace(',','')
                    self.new_prices.append(float(price))

        converted_prices(self, self.prices)
        print('Se cambio el tipo de dato de los precios.')
        self.new_prices_zero = [0 if a == '' else a for a in self.new_prices]

        for i,record in enumerate(self.records_list[1:]): #quitamos los headers
            converted_prices(self, record[4:-2]) # obtenemos los precios solamente 
            lista_zero = [0 if a == '' else a for a in self.new_prices]
            avg = round(statistics.mean([float(e) for e in lista_zero]),2)
            self.avg_list.append(avg)

            try:
                diff = round((((float(self.new_prices_zero[i])*100)/avg)-100),2)
            except:
                diff = 0
        
            if self.new_prices_zero[i] == 0:
                self.comments.append(f'⚠️ El articulo no esta disponible por el momento.')
            elif diff < 0:
                self.comments.append(f'✅ El articulo esta {diff}% mas bajo que el promedio de las ultimas semana.')
            elif diff > 0:
                self.comments.append(f'❗ El articulo esta {diff}% mas alto que el promedio de las ultimas semanas.')
            else:
                self.comments.append(f'❕ El articulo esta en el mismo precio que el promedio de las ultimas semanas.')


    #TODO: Agregar metodo para notificar cual ha sido el precio mas bajo desde que se ejecuta el programa.

    #TODO: Agregar metodo para solo buscar el precio para los articulos que no se encontraron

    #TODO: Agregar metodo para notificar al usuario por Correo cuando el producto este mas barato