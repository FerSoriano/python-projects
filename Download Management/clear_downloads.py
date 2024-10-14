# Programa para administrar la carpeta de descargas

from pathlib import Path
import shutil

DESCARGAS = '/Users/fersoriano/Downloads'

folderAudios        = DESCARGAS + '/Descargas_Audios'
folderEjecutables   = DESCARGAS + '/Descargas_Programas'
folderExcel         = DESCARGAS + '/Descargas_Excel'
folderImagenes      = DESCARGAS + '/Descargas_Imagenes'
folderOtros         = DESCARGAS + '/Descargas_Otros'
folderPDF           = DESCARGAS + '/Descargas_PDF'
folderVideos           = DESCARGAS + '/Descargas_Videos'

listExcel = ['.xls', '.xlsx', '.csv', '.xlsm']
listPDF   = ['.pdf']
listEXE   = ['.exe','.zip','.dmg','.iso', '.app']
listMusic = ['.mp3']
listVideo = ['.mp4','.mov']
listPhoto = ['.jpg', '.jpeg', '.png']

files_name = []
flag = 0

folders = {
    'Descargas_Audios' : 0,
    'Descargas_Programas': 0,
    'Descargas_Excel': 0,
    'Descargas_Imagenes': 0,
    'Descargas_Otros': 0,
    'Descargas_PDF': 0,
    'Descargas_Videos':0
}

def move_files(folder, file) -> None:
    global flag
    shutil.move(file, folder + '/' + file.name)
    files_name.append(file.name)
    folders[Path(folder).stem] += 1
    flag += 1
    return

def clear_downloads() -> None:

    pathFiles = Path(DESCARGAS)

    for e in pathFiles.iterdir():
        suf = e.suffix
        if suf == '' or suf == '.ini':
            continue
        elif suf in listExcel:
            move_files(folderExcel,e)
        elif suf in listPDF:
            move_files(folderPDF,e)
        elif suf in listEXE:
            move_files(folderEjecutables,e)
        elif suf in listMusic:
            move_files(folderAudios,e)
        elif suf in listPhoto:
            move_files(folderImagenes,e)
        elif suf in listVideo:
            move_files(folderVideos,e)
        elif not e.is_dir():
            move_files(folderOtros,e)
        else:
            print(f'Se encontro algun error en el archivo: {e.name}')
            exit()

def show_moved_files() -> None:
    if flag > 0:
        print('Done ✅ Se movieron los archivos.\n')
        for key, value in folders.items():
            if value > 0:
                print(f'{key} -> {value} archivo(s).')
        print('\n')
    else:
        print('No se encontraron archivos nuevos. 😴💤\n')

if __name__ == '__main__':
    clear_downloads()
    show_moved_files()
