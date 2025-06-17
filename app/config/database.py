import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import Optional
from app.models.url import Base


class DatabaseConfig:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "5432"))
        self.database = os.getenv("DB_NAME", "urlshortener")
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD", "password")
        self.connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class DatabaseConnection:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine = create_engine(
            config.connection_string,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            echo=False
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._session: Optional[Session] = None

    def get_session(self) -> Session:
        if self._session is None:
            self._session = self.SessionLocal()
        return self._session

    def close_session(self):
        if self._session:
            self._session.close()
            self._session = None

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def execute_migration(self, migration_sql: str):
        with self.engine.connect() as connection:
            connection.execute(migration_sql)
            connection.commit()


def create_database_connection() -> DatabaseConnection:
    config = DatabaseConfig()
    return DatabaseConnection(config)


def run_migrations(db_connection: DatabaseConnection):
    db_connection.create_tables()
