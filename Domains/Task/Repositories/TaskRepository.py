from Database.database import Database

class TaskRepository:
    def __init__(self, db: Database):
        self.db = db

    def get_all_tasks(self):
        return self.db.execute_command(
            """
            SELECT
                id,
                project_id,
                name,
                description,
                start_date,
                end_date
            FROM tasks
            ORDER BY project_id, id;
            """
        )
