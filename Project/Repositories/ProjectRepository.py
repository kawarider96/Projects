from database import Database

class ProjectRepository:
    def __init__(self, db: Database):
        self.db = db

    def get_all_project_data(self):
        return self.db.execute_command(
            """
                WITH RECURSIVE project_tree AS (
                    SELECT
                        id,
                        parent_id,
                        name,
                        description,
                        start_date,
                        end_date,
                        0 AS level
                    FROM projects
                    WHERE parent_id IS NULL

                    UNION ALL

                    SELECT
                        p.id,
                        p.parent_id,
                        p.name,
                        p.description,
                        p.start_date,
                        p.end_date,
                        pt.level + 1
                    FROM projects p

                    JOIN project_tree pt
                        ON p.parent_id = pt.id
                )

                SELECT *
                FROM project_tree
                ORDER BY level, id;
            """
        )