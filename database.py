import psycopg2
from Exceptions import DbConnectionError, DbExecutionError, WrongSqlCommandError

class Database:
    def __init__(self): #Az init a class létrehozásakor fut le, itt lehet inicializálni a class változóit
        self.conn = None #Van egy ilyen propja de kezdetben még nincs benne adatbázis kapcsolat
        
    def connect(self): 
        self.conn = psycopg2.connect(
            host="EXAMPLE",
            port=24936,
            database="defaultdb",
            user="avnadmin",
            password="PASSWORD",
            sslmode="require"
        )
    
    def execute_command(self, command, params=None):
        if self.conn is None:
            raise DbConnectionError("Nincs adatbázis kapcsolat.")
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(command, params)

                if cursor.description is not None:
                    return self.makeDictionary(cursor)
                
            self.conn.commit()
            return None
        
        except psycopg2.errors.SyntaxError as e:
            self.conn.rollback()

            raise WrongSqlCommandError(
                f"Hibás SQL szintaxis: {e}"
            )

        except psycopg2.Error as e:
            self.conn.rollback()

            raise DbExecutionError(
                f"Adatbázis hiba: {e}"
            )

    def execute_file(self, file_path):
        if self.conn is None:
            raise DbConnectionError("Nincs adatbázis kapcsolat.")
        
        with open(file_path, "r", encoding="utf-8") as file:
            sql = file.read()
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)

                result = None

                if cursor.description is not None:
                    return self.makeDictionary(cursor)
                
            self.conn.commit()
            return None

        except psycopg2.errors.SyntaxError as e:
            self.conn.rollback()

            raise WrongSqlCommandError(
                f"Hibás SQL szintaxis: {e}"
            )

        except psycopg2.Error as e:
            self.conn.rollback()

            raise DbExecutionError(
                f"Adatbázis hiba: {e}"
            )
    
    def makeDictionary(self, cursor):
        col_name = [
            column[0] for column in cursor.description
        ]

        result = [
            dict(zip(col_name, row)) for row in cursor
        ]

        return result
    
    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None