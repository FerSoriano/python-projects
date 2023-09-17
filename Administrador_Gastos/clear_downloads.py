# Programa para administrar la carpeta de descargas

from pathlib import Path
import shutil


def clear_downloads():
    descargas         = 'C:/Users/fer8f/Downloads'

    folderAudios      =  descargas + '/Descargas_Audios'
    folderEjecutables =  descargas + '/Descargas_Ejecutables'
    folderExcel       =  descargas + '/Descargas_Excel'
    folderImagenes    =  descargas + '/Descargas_Imagenes'
    folderOtros       =  descargas + '/Descargas_Otros'
    folderPDF         =  descargas + '/Descargas_PDF'

    listExcel = ['.xls','.xlsx','.csv', '.xlsm']
    listPDF = ['.pdf']
    listEXE = ['.exe']
    listMusic = ['.mp3','.mp4']
    listPhoto = ['.jpg','.jpeg', '.png']

    pathFiles = Path(descargas)

    for e in pathFiles.iterdir():
        suf = e.suffix
        if suf == '' or suf == '.ini':
            continue
        elif suf in listExcel:
            shutil.move(e, folderExcel + '/' + e.name)
        elif suf in listPDF:
            shutil.move(e, folderPDF + '/' + e.name)
        elif suf in listEXE:
            shutil.move(e, folderEjecutables + '/' + e.name)
        elif suf in listMusic:
            shutil.move(e, folderAudios + '/' + e.name)
        elif suf in listPhoto:
            shutil.move(e, folderImagenes + '/' + e.name)
        elif not e.is_dir():
                shutil.move(e, folderOtros + '/' + e.name)
        else:
            print('se encontro algun error.')
                

    print('Done. Se movieron los archivos.\n')


