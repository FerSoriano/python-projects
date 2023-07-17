import config
import gspread
import time
import os
from datetime import date

class PriceTracking():
    def __init__(self, service_account, workbook, worksheet):
        self.service_account = service_account
        self.workbook = workbook
        self.worksheet = worksheet

    def setConection(self):
        self.gc = gspread.service_account(self.service_account)
    
    def getRecords(self):
        self.wb = self.gc.open(self.workbook)
        self.ws = self.wb.worksheet(self.worksheet)
        self.records = self.ws.get_all_records()
        self.records_list = self.ws.get_all_values()
    
    def getPrices(self, data_dummy): # (self, records) -> self.records
        self.data_dummy = data_dummy # self.records = records
        self.prices = []

        for e in self.data_dummy:
            if e['Sitio'] == 'Amazon':
                try:
                    time.sleep(2)
                    driver = config.get_selenium_driver()
                    driver.get(e['URL'])
                    time.sleep(1)
                    price_element = driver.find_element(by='xpath', value='//*[@id="corePrice_feature_div"]/div/span[1]/span[2]/span[2]')
                    price = price_element.text
                    time.sleep(2)
                    driver.close()
                    self.prices.append(price)
                except:
                    driver.close()
                    print('No se encontro el precio.')
                    self.prices.append('')
        #TODO: completar el scraping de Mercado Libre.
            elif e['Sitio'] == 'Mercado Libre':
                continue
        
        os.system('cls')
        print(self.prices)

    # Metodo ejemplo, una vez funcione se agregara a getPrices()
    def getConvertedPrices(self, prices):
        self.prices = prices
        self.new_prices = []
        for price in self.prices:
            if price == '':
                self.new_prices.append(price)
            else:
                price = price.replace(',','')
                self.new_prices.append(float(price))
        # print(self.new_prices)
    
    def updateWorksheet(self):
        #TODO: obtener precios en modo lista -> self.records_list
        #TODO: sacar el promedio
        #TODO: investigar como obtener la ultima columna de la hoja
        
        # ejemplo manual
        today = str(date.today())
        new_prices = [[price] for price in self.new_prices]
        print(new_prices)
        self.ws.update('D:D', [[today]] + new_prices)
        print('Se actualizaron los precios.')




dummy = [
    {
        'Sitio': 'Amazon',
        'Articulo': 'Xiaomi Mi Computer Monitor Light Bar Negro', 
        'URL': 'https://www.amazon.com.mx/dp/B08W2C5W59/?coliid=IZ6HKOKHT1GNS&colid=P224OBRPAWZO&psc=0&ref_=list_c_wl_gv_ov_lig_pi_dp'
    },
     {'Sitio': 'Amazon', 'Articulo': 'Fender FA-115 Dreadnought - Guitarra acústica', 'URL': 'https://www.amazon.com.mx/dp/B07NMDYPVH/?coliid=I2JYG2V7805KUL&colid=P224OBRPAWZO&psc=1&ref_=list_c_wl_gv_ov_lig_pi_dp'}, {'Sitio': 'Amazon', 'Articulo': 'TERPORT Mouse Pad Antideslizante', 'URL': 'https://www.amazon.com.mx/dp/B0B1DBM4D6/?coliid=I66NMI7GX1VRT&colid=P224OBRPAWZO&ref_=list_c_wl_gv_ov_lig_pi_dp&th=1'}, {'Sitio': 'Amazon', 'Articulo': '7 en 1 Kit de Limpiador Cepillo', 'URL': 'https://www.amazon.com.mx/dp/B0BG82RXCX/?coliid=IEW1B1JSEWH9Z&colid=P224OBRPAWZO&ref_=list_c_wl_gv_ov_lig_pi_dp&th=1'}, {'Sitio': 'Amazon', 'Articulo': 'SUHOMMY Organizador Portátil, Bolsa de Doble Capa para Accesorios Electrónicos', 'URL': 'https://www.amazon.com.mx/dp/B096SBV42G/?coliid=I1I5PO67YO9156&colid=P224OBRPAWZO&ref_=list_c_wl_gv_ov_lig_pi_dp&th=1'}, {'Sitio': 'Amazon', 'Articulo': 'Nouhaus ErgoTASK - Silla de trabajo ergonómica', 'URL': 'https://www.amazon.com.mx/dp/B084DF5SBQ/?coliid=I33O51B5W9ZT50&colid=P224OBRPAWZO&ref_=list_c_wl_gv_ov_lig_pi_dp&th=1'}, {'Sitio': 'Mercado Libre', 'Articulo': 'Guitarra acústica Fender Classic Design CC-60S ', 'URL': 'https://www.mercadolibre.com.mx/guitarra-acustica-fender-classic-design-cc-60s-para-diestros-all-mahogany-brillante/p/MLM15489106#polycard_client=bookmarks'}, {'Sitio': 'Mercado Libre', 'Articulo': 'Fender Concert Cc-60s Paquete Guitarra Acústica All Mahogany', 'URL': 'https://articulo.mercadolibre.com.mx/MLM-1502021954-fender-concert-cc-60s-paquete-guitarra-acustica-all-mahogany-_JM#polycard_client=bookmarks'}, {'Sitio': 'Mercado Libre', 'Articulo': 'Paquete Guitarra Acústica Fender Concert Cc-60s All Mahogany', 'URL': 'https://articulo.mercadolibre.com.mx/MLM-1502083549-paquete-guitarra-acustica-fender-concert-cc-60s-all-mahogany-_JM#polycard_client=bookmarks'}, {'Sitio': 'Mercado Libre', 'Articulo': 'Bicicleta De Ruta Gravel Armstrong R700 Shimano A070 14v', 'URL': 'https://articulo.mercadolibre.com.mx/MLM-1796834734-bicicleta-de-ruta-gravel-armstrong-r700-shimano-a070-14v-_JM#polycard_client=bookmarks'}, {'Sitio': 'Mercado Libre', 'Articulo': 'Soporte De Correa De Arnés De Montaje En El Pecho Del Teléfo', 'URL': 'https://articulo.mercadolibre.com.mx/MLM-1397525381-soporte-de-correa-de-arnes-de-montaje-en-el-pecho-del-telefo-_JM#polycard_client=bookmarks'}
]

precios_dummy = ['', '4,175', '245', '185', '169', '5,072']

app = PriceTracking(service_account=config.get_service_account(), workbook='Price Tracking', worksheet='app')
######################
app.setConection()
app.getRecords()
######################

# app.getPrice(dummy)
app.getConvertedPrices(precios_dummy)
app.updateWorksheet()