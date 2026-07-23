
class DatabaseInfoCommands:
    def __init__(self, db):
        self.db = db

    def table_info(self, command):
        target = command.split(" ", 1)[1]

        return self.db.execute_command(
            f"""
            SELECT
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = 'public'
                AND table_name = %s
            ORDER BY ordinal_position;
            """,
            (target,)
        )
    
    def db_info(self):
        return self.db.execute_command(
            """
            SELECT
                current_database() AS database_name,
                current_user AS user_name,
                current_schema() AS schema_name,
                pg_size_pretty(
                    pg_database_size(current_database())
                ) AS database_size,
                version() AS postgres_version;
            """
        )
    
    def tables(self):
        return self.db.execute_command(
            """
            SELECT
                table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
            """
        )