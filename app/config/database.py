import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional


class DatabaseConfig:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "5432"))
        self.database = os.getenv("DB_NAME", "urlshortener")
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD", "password")
        self.connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    def get_connection_params(self) -> dict:
        return {
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "user": self.user,
            "password": self.password,
            "cursor_factory": RealDictCursor
        }


class DatabaseConnection:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._connection: Optional[psycopg2.extensions.connection] = None

    def connect(self):
        if self._connection is None or self._connection.closed:
            self._connection = psycopg2.connect(**self.config.get_connection_params())
            self._connection.autocommit = False
        return self._connection

    def close(self):
        if self._connection and not self._connection.closed:
            self._connection.close()

    def cursor(self):
        connection = self.connect()
        return connection.cursor()

    def commit(self):
        if self._connection and not self._connection.closed:
            self._connection.commit()

    def rollback(self):
        if self._connection and not self._connection.closed:
            self._connection.rollback()

    def execute_migration(self, migration_sql: str):
        cursor = self.cursor()
        try:
            cursor.execute(migration_sql)
            self.commit()
        except Exception as e:
            self.rollback()
            raise e
        finally:
            cursor.close()


def create_database_connection() -> DatabaseConnection:
    config = DatabaseConfig()
    return DatabaseConnection(config)


def run_migrations(db_connection: DatabaseConnection):
    migrations_dir = os.path.join(os.path.dirname(__file__), "../../migrations")
    
    if not os.path.exists(migrations_dir):
        return
    
    migration_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith('.sql')])
    
    for migration_file in migration_files:
        migration_path = os.path.join(migrations_dir, migration_file)
        with open(migration_path, 'r') as f:
            migration_sql = f.read()
        
        try:
            db_connection.execute_migration(migration_sql)
            print(f"Applied migration: {migration_file}")
        except Exception as e:
            print(f"Error applying migration {migration_file}: {e}")
            raise