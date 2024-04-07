
import requests
import pandas as pd
import os
import gspread
from gspread_dataframe import set_with_dataframe
import random


class Download_Movie_List():
    def __init__(self, url, headers) -> None:
        self.url = url
        self.headers = headers

    def get_movie_list(self):
        self.respuesta = requests.get(self.url, headers=self.headers)

        # se busca la tabla que haga match con algun texto dentro mi la tabla
        matched_table = pd.read_html(self.respuesta.text, match='Director')

        self.movies = matched_table[0]

        self.movies.columns = ['No', 'Title', 'Director','Year']
        self.movies.drop(self.movies.tail(2).index, inplace=True)

        self.movies.set_index('No', inplace=True)

        return self.movies


class Google_Conection(Download_Movie_List):
    """
    esta clase debera ser capaz de leer subir la lista de las pelis, de leerlas y actualizarlas
    """
    def __init__(self, url, headers, workbook, worksheet) -> None:
        super().__init__(url, headers)
        self.workbook = workbook
        self.worksheet = worksheet
    
    def setConection(self):
        path = os.getcwd()
        service_account = path + '/key/key.json'
        gc = gspread.service_account(service_account) # gc = google conection
        wb = gc.open(self.workbook)
        self.ws = wb.worksheet(self.worksheet)

    def updateWorksheet(self):
        self.ws.clear()
        set_with_dataframe(worksheet=self.ws,
                           dataframe=self.file,
                           include_index=True,
                           include_column_header=True,
                           resize=False,)

    def getRecords(self):
        self.records = self.ws.get_all_records()
        self.records_list = self.ws.get_all_values()

        self.df_temp = pd.DataFrame(self.records)
        self.df_temp.set_index('No', inplace=True)

        return self.df_temp


class Movies(Google_Conection):
    def __init__(self, url, headers, workbook, worksheet) -> None:
        super().__init__(url, headers, workbook, worksheet)
        
    def create_csv(self, file_name, file_type):
        """
        1 = Guardar lista original - Wikipedia\n
        2 = Guardar el archivo temp - Google Sheets\n
        3 = Guardar el archivo temp actualizado - Pelicula vista
        """
        if file_type == 1:
            self.movies.to_csv(file_name)
        elif file_type == 2:
            self.df_temp.to_csv(file_name)
        elif file_type == 3:
            self.csv_updated.to_csv(file_name)
        else:
            Exception({'msg': 'Opcion invalida'})

    def read_csv(self, file_name, file_type = 0):
        self.file = pd.read_csv(file_name)
        self.file.set_index('No', inplace=True)
        if file_type == 1: # para agregar la bandera 'Valid'
            max_rows = len(self.file.index)
            valid_column = ['N' for row in range(1,max_rows+1)] # agrega la bandera de 'N' cuando se ejecuta por primera vez
            self.file['Valid'] = valid_column
        return self.file
    
    def select_random_movie(self, file_name):
        self.csv_updated = self.read_csv(file_name=file_name)
        unwatched_movies = self.csv_updated[self.csv_updated['Valid'] == 'N'].index.tolist()
        random_number = random.choice(unwatched_movies)
        self.csv_updated.at[random_number, 'Valid'] = 'Y'
        self.movie_selected = self.csv_updated.filter(items=[random_number], axis=0) #sera usado para notificar al usuario
        # self.movie_selected.set_index(drop=True)
        return self.csv_updated
    

    def notify_user(self):
        title = self.movie_selected['Title'].values.tolist()[0]
        director = self.movie_selected['Director'].values.tolist()[0]
        year = self.movie_selected['Year'].values.tolist()[0]
        message = f'\nTenemos la pelicula para hoy!🍿🎬 \nLa pelicula elegida fue...👀\n\n\tTitulo: {title}\n\tDirector: {director}\n\tYear: {year}\n'
        print(message)




