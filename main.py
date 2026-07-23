from database import Database
from pprint import pprint
import json
from Exceptions import WrongSqlCommandError, DbConnectionError, DbExecutionError
from Helpers.dbCommands import DatabaseInfoCommands
from Project.Controller.ProjectController import ProjectController
from Project.Repositories.ProjectRepository import ProjectRepository
from Project.Services.ProjectService import ProjectService  

db = Database()
db_info_commands = DatabaseInfoCommands(db)
ProjectRepo = ProjectRepository(db)
ProjectService = ProjectService(ProjectRepo)
project = ProjectController(ProjectService)

try:
    db.connect()

except DbConnectionError as e:
    print(e)
    exit()

while True:
    command = input("> ")

    if command == "exit":
        break

    try:
        if command.startswith("/table_info "):

            result = db_info_commands.table_info(command)

        elif command == "/db_info":
            result = db_info_commands.db_info()

        elif command == "/tables":
            result = db_info_commands.tables()

        elif command == "get_all_project":
            result = project.get_all_project()

        else:
            result = db.execute_command(command)

        if result is not None:
            print(
                json.dumps(
                    result,
                    indent=4,
                    default=str,
                    ensure_ascii=False
                )
            )

    except WrongSqlCommandError as e:
        print(e)

    except DbConnectionError as e:
        print(e)

    except DbExecutionError as e:
        print(e)

    except Exception as e:
        print(f"Ismeretlen hiba: {e}")