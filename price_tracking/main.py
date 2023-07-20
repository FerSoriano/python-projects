"""
Scrip to get and track prices (Amazon / Mercado libre wishlist) week over week.
The data is stored in a private Google SpreadSheet.
You will be able to see the behaivor of each item.
"""

import config
import gspread
import time
import os
from datetime import date
import statistics

class PriceTracking():
    def __init__(self, service_account, workbook, worksheet):
        self.service_account = service_account
        self.workbook = workbook
        self.worksheet = worksheet
        self.start = time.time()

    def setConection(self):
        self.gc = gspread.service_account(self.service_account)
    
    def getRecords(self):
        self.wb = self.gc.open(self.workbook)
        self.ws = self.wb.worksheet(self.worksheet)
        self.records = self.ws.get_all_records()
        self.records_list = self.ws.get_all_values()
    
    def getPrices(self):         
        self.prices = []

        def execute_selenium(self, url, xpath):
            try:
                time.sleep(2)
                driver = config.get_selenium_driver()
                driver.get(url)
                time.sleep(2)
                price_element = driver.find_element(by='xpath', value=xpath)
                price = price_element.text
                time.sleep(2)
                driver.close()
                self.prices.append(price)
                print(price)
            except:
                driver.close()
                print('No se encontro el precio.')
                self.prices.append('')

        for e in self.records:
            if e['Sitio'] == 'Amazon':
                self.xpath = '//*[@id="corePrice_feature_div"]/div/span[1]/span[2]/span[2]'
            elif e['Sitio'] == 'Mercado Libre':
                if e['Articulo'] == 'Guitarra acústica Fender Classic Design CC-60S':
                    self.xpath = '//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[1]/span/span[3]'
                else:
                    self.xpath = '//*[@id="price"]/div/div[1]/div[1]/span/span[3]'
            execute_selenium(self, url=e['URL'], xpath=self.xpath)

        os.system('cls')
        print('Se extrajeron los precios de los articulos.')

    
    def updateWorksheet(self):
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
            print('Se cambio el tipo de dato de los precios.')

        converted_prices(self, self.prices)
        new_prices_zero = [0 if a == '' else a for a in self.new_prices]

        for i,record in enumerate(self.records_list[1:]): #quitamos los headers
            converted_prices(self, record[3:-2]) # obtenemos los precios solamente 
            lista_zero = [0 if a == '' else a for a in self.new_prices]
            avg = round(statistics.mean([float(e) for e in lista_zero]),2)
            self.avg_list.append(avg)

            try:
                diff = round((((float(new_prices_zero[i])*100)/avg)-100),2)
            except:
                diff = 0
        
            if diff < 0:
                self.comments.append(f'✅ El articulo esta {diff}% mas bajo que el promedio de las ultimas semana.')
            elif diff > 0:
                self.comments.append(f'❗ El articulo esta {diff}% mas alto que el promedio de las ultimas semanas.')
            elif new_prices_zero[i] == 0:
                self.comments.append(f'⚠️ El articulo no esta disponible por el momento.')
            else:
                self.comments.append(f'❕ El articulo esta en el mismo precio que el promedio de las ultimas semanas.')

        today = str(date.today())
        new_prices = [price for price in new_prices_zero]
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

        print('Se actualizaron los precios correctamente en Google Sheets.')
        self.end = time.time()
        print(f'Tiempo total de ejecucion: {round((self.end - self.start),2)} seg.')
            

app = PriceTracking(service_account=config.get_service_account(), workbook='Price Tracking', worksheet='app')
app.setConection()
app.getRecords()
app.getPrices()
app.updateWorksheet()

