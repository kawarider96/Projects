import psycopg2
from Exceptions.Exceptions import DbConnectionError, DbExecutionError, WrongSqlCommandError
import os
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH)



class Database:
    def __init__(self): #Az init a class létrehozásakor fut le, itt lehet inicializálni a class változóit
        self.conn = None #Van egy ilyen propja de kezdetben még nincs benne adatbázis kapcsolat
        
    def connect(self): 
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                sslmode="require"
            )
        except psycopg2.Error as e:
            raise DbConnectionError(
                f"Nem sikerült kapcsolódni az adatbázishoz: {e}"
            ) from e
    
    def execute_command(self, command, params=None):
        if self.conn is None:
            raise DbConnectionError("Nincs adatbázis kapcsolat.")
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(command, params)

                if cursor.description is not None:
                    return self.make_dictionary(cursor)
                
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

                if cursor.description is not None:
                    return self.make_dictionary(cursor)
                
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
    
    def make_dictionary(self, cursor):
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