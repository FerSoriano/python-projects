from datetime import datetime
import csv

from db.config import load_config
from db.connect import DatabaseConection
from etl.olympics_medals import Medals

config = load_config()
db = DatabaseConection(config=config)
db.connect()

CREATE_SCHEMAS = True
CREATE_TABLES = True
TEST_CSV = False
RUN_ETL = True

if CREATE_SCHEMAS:
    db.create_schemas()

if CREATE_TABLES:
    db.create_stage_table_executionLog()
    db.create_stage_table_medallero()
    db.create_edw_table_medallero()

last_execution = db.get_last_execution()
today = datetime.now().strftime("%Y-%m-%d")

if today == str(last_execution):
    print('Ya se actualizo el dia de hoy.')
    exit()

if TEST_CSV:
    with open('medals.csv', mode='r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

if RUN_ETL:
    medals = Medals()
    medals.get_response()
    df = medals.get_medals()

    # Truncar Stage
    db.truncate_stage_table_medallero()
    # Insertar Stage
    db.insert_to_stage_table_medallero(df=df)
    # Insertar Execution Log
    db.insert_to_stage_table_executionlog(today)
    # Actualizar Is_Active a 0
    db.update_edw_table_medallero()
    # Insertar en EDW
    db.insert_to_edw_table_medallero()

print('ETL process completed successfully...')