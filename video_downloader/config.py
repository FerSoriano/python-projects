
"""
Codigo para descargar videos de Youtube.
Se almacenaran en la carptera correspondiente a cada episodio.
Las URL de los videos se obtendran de un libro de Google Sheets.
"""
import os
import csv
import time
import shutil
import gspread
from pytube import YouTube
import pandas as pd
from gspread.auth import ServiceAccountCredentials

def get_service_account():
    service_account = '/Users/fersoriano/Documents/Proyectos/Podcast/code/key/key.json'
    return service_account

class GoogleConnection():
    def __init__(self, service_account, workbook, worksheet, csv) -> None:
        """
        Se settea la cuenta de servicio de google y se selecciona libro y hoja.
        """
        self.service_account = service_account
        self.workbook = workbook
        self.worksheet = worksheet
        self.csv = csv
        self.start = time.time()

    def setConection(self) -> None:
        scope = ["https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"]
        
        credentials = ServiceAccountCredentials.from_service_account_file(
            self.service_account, scopes=scope)
        
        self.gc = gspread.authorize(credentials)

    def getRecords(self) -> None:
        try:
            self.wb = self.gc.open(self.workbook)
            self.ws = self.wb.worksheet(self.worksheet)
            self.records = self.ws.get_all_records()
        except gspread.exceptions.APIError as e:
            print(f"Error de API de Google Sheets: {e}")

    def moveDataToCSV(self,episodio) -> None:
        os.system('clear')
        df = pd.DataFrame(self.records)
        df = df[df.Episodio == episodio]
        df.to_csv(self.csv, index=False)
        print('Se actualizo el CSV 📝\n')

class DescargaVideos(): 
    def __init__(self, file) -> None:
        self.file = file
        self.temp = './temp/'

    def getURLs(self) -> list:
        self.urls = []
        self.titulos = []
        with open(self.file,'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            for line in csv_reader:
                self.urls.append(line[1])
                self.titulos.append(line[2])
        return self.urls
    
    def getExecutionTime(self) -> None:
        total_time = round((self.end - self.start),2)
        unidad = 'seg'
        if total_time > 60:
            total_time = round((total_time / 60),2)
            unidad = 'min'
        print(f'Tiempo total de descarga: {str(total_time)} {unidad}.\n')
        
    
    def download(self,path_videos) -> None:
        urls = self.getURLs()
        for e,url in enumerate(urls):
            self.start = time.time()
            print('Intentando conectar a Youtube...')
            video = YouTube(url)
            print('Obteniendo informacion del video...')
            download_video = video.streams.get_highest_resolution()
            try:
                print(f'Descargando video {e+1}...')
                download_video.download(self.temp)
                print(f'Se descargo el video: {self.titulos[e]} con exito! ✅')
                self.end = time.time()
                self.getExecutionTime()
                self.move(path_videos,self.titulos[e])
            except:
                print(f'Sucedio un error en descargar el video {self.titulos[e]} ❌')
        

    def move(self,path,name) -> None:
        for e in os.listdir(self.temp):
            if e.endswith('.mp4'):
                shutil.move(self.temp + '/' + e, path + '/' + name + '.mp4')



