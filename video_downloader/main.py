
import config
import os

EPISODIO = 'Ep-01'
WORKBOOK = 'Futbol-Champagne'
WORKSHEET = 'videos'
CSV = 'videos.csv'
PATH_VIDEOS = f'/Users/fersoriano/Documents/Proyectos/Podcast/videos/{EPISODIO}/downloads'


texto = f"""
*** Episodio actual: {EPISODIO} ***
Esta correcto el Episodio? ('y' para continuar o cualquiera para salir): """

r = input(texto).lower()

audio = False
solo_audio = input("Deseas descargar solo el audio? 'y' para continuar o cualquiera para omitir): ").lower()
if solo_audio == 'y':
    audio = True

if r == 'y':
    conexion = config.GoogleConnection(service_account=config.get_service_account(),workbook=WORKBOOK,worksheet=WORKSHEET,csv=CSV)
    conexion.setConection()
    conexion.getRecords()
    conexion.moveDataToCSV(EPISODIO)

    videos = config.DescargaVideos(CSV)
    videos.download('.',audio=audio)

    print('Proceso completado.')

else:
    os.system('clear')
    exit()