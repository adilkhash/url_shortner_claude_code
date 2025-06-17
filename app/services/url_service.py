import secrets
import string
from datetime import datetime
from typing import Optional
from app.models.url import URLModel
from app.repositories.url_repository import URLRepository


class URLService:
    def __init__(self, repository: URLRepository):
        self.repository = repository

    def generate_short_code(self, length: int = 6) -> str:
        characters = string.ascii_letters + string.digits
        max_attempts = 10
        
        for _ in range(max_attempts):
            short_code = ''.join(secrets.choice(characters) for _ in range(length))
            existing_url = self.repository.get_by_short_code(short_code)
            if not existing_url:
                return short_code
        
        raise Exception("Failed to generate unique short code after maximum attempts")

    def create_url(
        self,
        original_url: str,
        custom_code: Optional[str] = None,
        expires_at: Optional[datetime] = None
    ) -> URLModel:
        if custom_code:
            existing_url = self.repository.get_by_short_code(custom_code)
            if existing_url:
                raise ValueError(f"Short code '{custom_code}' already exists")
            short_code = custom_code
        else:
            short_code = self.generate_short_code()

        url = URLModel(
            original_url=original_url,
            short_code=short_code,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
            is_active=True
        )

        return self.repository.create(url)

    def get_url_by_short_code(self, short_code: str) -> Optional[URLModel]:
        return self.repository.get_by_short_code(short_code)

    def get_url_by_id(self, url_id: int) -> Optional[URLModel]:
        return self.repository.get_by_id(url_id)

    def increment_click_count(self, url_id: int) -> Optional[URLModel]:
        return self.repository.increment_click_count(url_id)

    def is_url_expired(self, url: URLModel) -> bool:
        if not url.expires_at:
            return False
        return datetime.utcnow() > url.expires_at

    def deactivate_url(self, url_id: int) -> bool:
        return self.repository.deactivate_url(url_id)

    def cleanup_expired_urls(self) -> int:
        return self.repository.cleanup_expired_urls()