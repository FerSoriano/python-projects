from settings import Movies

URL = 'https://es.wikipedia.org/wiki/Anexo:Las_100_mejores_pel%C3%ADculas_del_siglo_XXI_seg%C3%BAn_la_BBC'
HEADERS = {"User-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
WORKBOOK = 'movie time'
WORKSHEET = 'Top Movies'
CSV_NAME = '100 mejores peliculas siglo XXI.csv'
CSV_TEMP = 'temp.csv'

movies = Movies(url=URL, headers=HEADERS, workbook=WORKBOOK, worksheet=WORKSHEET)

# flags
full_process = False
select_movie = True
is_test = False


# validations
if not full_process and not select_movie and not is_test:
    print('Banderas apagadas.\nFin del programa.')
    exit()

if full_process and select_movie:
    print('No puede haber dos o mas banderas prendidas.\nFin del programa.')
    exit()
elif full_process and is_test:
    print('No puede haber dos o mas banderas prendidas.\nFin del programa.')
    exit()
elif select_movie and is_test:
    print('No puede haber dos o mas banderas prendidas.\nFin del programa.')
    exit()


if full_process:
    print('descargando la lista desde Wikipedia...🌐')
    # obetenemos la lista desde la URL (wikipedia)
    movies.get_movie_list()
    # creamos el CSV original (se ejecuta solo la primera vez o cada que se quiera sobreescribir la lista original)
    movies.create_csv(file_name=CSV_NAME,file_type=1)
    # Creamos la conexion
    print('buscando nueva pelicula...🥸')
    movies.setConection()
    # leemos el CSV, se crea el df para despues poder subirlo a Google Sheets
    movies.read_csv(file_name=CSV_NAME,file_type=1) 
    # Actualizamos libro con la informacion del CSV
    movies.updateWorksheet()
    # Obtenemos los datos de GoogleSheets
    movies.getRecords()
    # Creamos el CSV temp con los datos descargados de GoogleSheets
    movies.create_csv(file_name=CSV_TEMP,file_type=2)
    # leemos el CSV temp y seleccionamos una pelicula aleatoria
    movies.select_random_movie(file_name=CSV_TEMP)
    # Creamos el CSV temp con los datos actualizados de la pelicula seleccionada
    movies.create_csv(file_name=CSV_TEMP,file_type=3)
    # leemos el CSV temp, se crea el df para despues poder subirlo a Google Sheets
    movies.read_csv(file_name=CSV_TEMP)
    # Actualizamos libro con la informacion del CSV
    movies.updateWorksheet()
    # Avisamos al Usuario que Pelicula ver
    movies.notify_user()
    
    exit()


if select_movie:
    print('buscando nueva pelicula...🥸')
    # Creamos la conexion
    movies.setConection()
    # Obtenemos los datos de GoogleSheets
    movies.getRecords()
    # Creamos el CSV temp con los datos descargados de GoogleSheets
    movies.create_csv(file_name=CSV_TEMP,file_type=2)
    # leemos el CSV temp y seleccionamos una pelicula aleatoria
    movies.select_random_movie(file_name=CSV_TEMP)
    # Creamos el CSV temp con los datos actualizados de la pelicula seleccionada
    movies.create_csv(file_name=CSV_TEMP,file_type=3)
    # leemos el CSV temp, se crea el df para despues poder subirlo a Google Sheets
    movies.read_csv(file_name=CSV_TEMP)
    # Actualizamos libro con la informacion del CSV
    movies.updateWorksheet()
    # Avisamos al Usuario que Pelicula ver
    movies.notify_user()

    exit()

if is_test:
    print('corriendo test...⚠️')
    # movies.create_csv(file_name=CSV_TEMP,file_type=2)
    movies.select_random_movie(file_name=CSV_TEMP)
    movies.notify_user()
    
    exit()
