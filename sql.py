from database import Database

db = Database()

try:
    db.connect()

    result = db.execute_file("command.sql")

    if result:
        for row in result:
            print(row)
    
except(Exception):
    raise

finally:
    db.close()