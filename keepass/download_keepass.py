import io
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


load_dotenv()


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
FOLDER_ID = os.getenv('FOLDER_ID')
DESTINATION_FILE = os.getenv('DESTINATION_FILE')


def autenticar_drive():
    """Autentica usando el archivo JSON de la cuenta de servicio."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)


def obtener_id_archivo_kdbx(service, folder_id):
    """Busca un archivo .kdbx dentro de la carpeta especificada."""
    query = f"'{folder_id}' in parents and name contains '.kdbx' and trashed = false"
    
    print(f"Buscando archivo .kdbx en la carpeta con ID: {folder_id}...")
    
    results = service.files().list(
        q=query, 
        fields="files(id, name)",
        pageSize=1
    ).execute()
    
    archivos = results.get('files', [])
    
    if not archivos:
        raise FileNotFoundError("No se encontró ningún archivo con extensión .kdbx dentro de esa carpeta.")
    
    archivo_encontrado = archivos[0]
    print(f"¡Archivo detectado! Nombre: {archivo_encontrado['name']} | ID: {archivo_encontrado['id']}")
    return archivo_encontrado['id']


def descargar_archivo(service, file_id, dest_path):
    """Descarga el archivo desde Drive usando su ID obtenido."""
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(dest_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    print("Iniciando la descarga del archivo binario...")
    
    while done is False:
        status, done = downloader.next_chunk()
        if status:
            print(f"Progreso de descarga: {int(status.progress() * 100)}%")
            
    print(f"¡Sincronización completada! Archivo guardado como: {dest_path}")


if __name__ == '__main__':
    try:
        if not SERVICE_ACCOUNT_FILE or not FOLDER_ID or not DESTINATION_FILE:
            raise ValueError(
                "Las variables de entorno no están configuradas correctamente. "
                "Asegúrate de completar el archivo .env"
            )
        
        drive_service = autenticar_drive()
        
        id_del_archivo = obtener_id_archivo_kdbx(drive_service, FOLDER_ID)
        
        descargar_archivo(drive_service, id_del_archivo, DESTINATION_FILE)
        
    except Exception as e:
        print(f"Ocurrió un error durante la ejecución: {e}")
