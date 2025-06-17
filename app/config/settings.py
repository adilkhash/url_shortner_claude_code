import os
from typing import Optional


class Settings:
    def __init__(self):
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", "8000"))
        self.base_url = os.getenv("BASE_URL", f"http://{self.host}:{self.port}")
        
        # Database settings
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = int(os.getenv("DB_PORT", "5432"))
        self.db_name = os.getenv("DB_NAME", "urlshortener")
        self.db_user = os.getenv("DB_USER", "postgres")
        self.db_password = os.getenv("DB_PASSWORD", "password")
        
        # URL shortening settings
        self.short_code_length = int(os.getenv("SHORT_CODE_LENGTH", "6"))
        self.max_url_length = int(os.getenv("MAX_URL_LENGTH", "2048"))
        
        # Security settings
        self.allowed_origins: list[str] = []
        origins_str = os.getenv("ALLOWED_ORIGINS", "")
        if origins_str:
            self.allowed_origins = [origin.strip() for origin in origins_str.split(",")]

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()