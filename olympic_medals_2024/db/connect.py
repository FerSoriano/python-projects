import psycopg2

class DatabaseConection():
    def __init__(self, config) -> None:
        self.config = config

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # connecting to the PostgreSQL server
            with psycopg2.connect(**self.config) as self.conn:
                print('Connected to the PostgreSQL server.')
                return self.conn
        except (Exception, psycopg2.DatabaseError ) as error:
            print(error)
            print('Error: connect()')
            exit()

    def create_schemas(self):
        """ Create schemas in the database """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("CREATE SCHEMA IF NOT EXISTS stage;")
                cursor.execute("CREATE SCHEMA IF NOT EXISTS edw;")
                self.conn.commit()
                print("Schemas created successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('Error: create_schemas()')
            self.conn.rollback()
            exit()

    def create_stage_table_executionLog(self):
        """ Create a table in the database """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS stage.executionLog (
                    id SERIAL PRIMARY KEY,
                    last_execution date not null
                );
                """)
                self.conn.commit()
                print("Table stage.executionLog created successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('Error: create_stage_table_executionLog()')
            self.conn.rollback()
            exit()

    def create_stage_table_medallero(self):
        """ Create stage table in the database """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS stage.medallero (
                    id SERIAL PRIMARY KEY,
                    rank INTEGER,
                    country varchar(255),
                    gold INTEGER,
                    silver INTEGER,
                    bronze INTEGER,
                    total INTEGER,
                    execution_date date not null
                );
                """)
                self.conn.commit()
                print("Table stage.medallero created successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('Error: create_stage_table_medallero()')
            self.conn.rollback()
            exit()

    def create_edw_table_medallero(self):
        """ Create edw table in the database """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS edw.medallero (
                    id SERIAL PRIMARY KEY,
                    rank INTEGER,
                    country varchar(255),
                    gold INTEGER,
                    silver INTEGER,
                    bronze INTEGER,
                    total INTEGER,
                    execution_date date not null,
                    is_active INTEGER not null,
                    country_id INTEGER
                );
                """)
                self.conn.commit()
                print("Table edw.medallero created successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('Error: create_edw_table_medallero()')
            self.conn.rollback()
            exit()

    def get_last_execution(self):
        """ Get the last execution """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT MAX(last_execution) FROM stage.executionlog;")
                last_execution = cursor.fetchone()
                print("get_last_execution() -> Data queried successfully")
                return last_execution[0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('Error: get_last_execution()')
            exit()

    def insert_to_stage_table_medallero(self, df):
        """ Insert DataFrame into PostgreSQL table """
        try:
            with self.conn.cursor() as cursor:
                for index, row in df.iterrows():
                    # Construir la sentencia SQL de inserción
                    cursor.execute(f"""
                        INSERT INTO stage.medallero (rank, country, gold, silver, bronze, total, execution_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (index, row['Country'], row['Gold'], row['Silver'], row['Bronze'], row['Total'], row['execution_date']))
                self.conn.commit()
                print("Data inserted successfully into stage.medallero.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('Error: insert_to_stage_table_medallero()')
            self.conn.rollback()
            exit()

    def truncate_stage_table_medallero(self):
        """ Truncate stage table """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("TRUNCATE table stage.medallero;")
                self.conn.commit()
                print("truncate_stage_table_medallero() -> executed successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('Error: truncate_stage_table_medallero()')
            self.conn.rollback()
            exit()

    def insert_to_stage_table_executionlog(self, last_execution):
        """ Insert last execution date """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"""
                        INSERT INTO stage.executionlog (last_execution)
                        VALUES (%s)
                    """, (last_execution,))
                self.conn.commit()
                print("Data inserted successfully into stage.executionLog.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('Error: insert_to_stage_table_executionlog()')
            self.conn.rollback()
            exit()

    def update_edw_table_medallero(self):
        """ Update Is_Active to Zero """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("UPDATE edw.medallero SET is_active = 0 WHERE is_active = 1;")
                self.conn.commit()
                print("update_edw_table_medallero() -> executed successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('Error: update_edw_table_medallero()')
            self.conn.rollback()
            exit()

    def insert_to_edw_table_medallero(self):
        """ Insert into EDW table """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO edw.medallero(
                            rank,
                            country,
                            gold,
                            silver,
                            bronze,
                            total,
                            execution_date,
                            is_active,
                            country_id
                        )
                            SELECT
                                rank, 
                                m.country,
                                gold,
                                silver,
                                bronze,
                                total,
                                execution_date,
                                1 as is_active,
                                c.id as "country_id"
                            FROM stage.medallero m
                            LEFT JOIN edw.countries c 
		                        ON c.country = m.country;
                    """)
                self.conn.commit()
                print("Data inserted successfully into edw.medallero.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('Error: insert_to_edw_table_medallero()')
            self.conn.rollback()
            exit()

    def create_edw_table_countries(self):
        """ Create Country table in the database """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS edw.countries (
                    id SERIAL PRIMARY KEY,
                    country varchar(255) not null
                );
                """)
                self.conn.commit()
                print("Table edw.Countries created successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('Error: create_edw_table_countries()')
            self.conn.rollback()
            exit()

    def insert_to_edw_table_countries(self):
        """ Insert into EDW table """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO edw.countries (country)
                    SELECT DISTINCT country 
                    FROM stage.medallero m
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM edw.countries c
                        WHERE c.country = m.country
                        )
                    ORDER BY 1 ASC;
                    """)
                self.conn.commit()
                print("Data inserted successfully into edw.countries.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('Error: insert_to_edw_table_countries()')
            self.conn.rollback()
            exit()