import os
import shutil
import time
from pytube import YouTube

class DescargaVideos(): 
    def __init__(self, url) -> None:
        self.url = url
        self.temp = './temp/'
    
    def getExecutionTime(self) -> None:
        total_time = round((self.end - self.start),2)
        unidad = 'seg'
        if total_time > 60:
            total_time = round((total_time / 60),2)
            unidad = 'min'
        print(f'Tiempo total de descarga: {str(total_time)} {unidad}.\n')
        
    
    def download(self,path_videos,audio) -> None:
        tipo = 'audio' if audio == True else 'video' 
        self.start = time.time()
        print('Intentando conectar a Youtube...')
        video = YouTube(self.url)
        print('Obteniendo informacion del video...')
        if audio == True:
            download_video = video.streams.get_audio_only()
        else:
            download_video = video.streams.get_highest_resolution()
        try:
            print(f'Descargando {tipo}...')
            download_video.download(self.temp)
            print(f'Se descargo el {tipo} con exito! ✅')
            self.end = time.time()
            self.getExecutionTime()
            path_from = self.temp + download_video.title + '.mp4'
            path_to = path_videos + download_video.title + '.mp4'
            shutil.move(path_from, path_to)
            
        except:
            print(f'Sucedio un error en descargar el {tipo}: {download_video.title} ❌')
            exit()

audio = False
url = input('URL del video: ')
solo_audio = input("Deseas descargar solo el audio? (y/n): ").lower()
path_videos = input("Donde deseas guardarlo? (default: ~/Movies/Downloaded): ")

if solo_audio == 'y':
    audio = True
elif solo_audio != 'n':
    print('Opcion incorrecta. ❌')
    exit()

if path_videos == '':
    path_videos = '/Users/fersoriano/Movies/Downloaded/'

videos = DescargaVideos(url)
videos.download(path_videos,audio=audio)

print('Proceso completado.')
