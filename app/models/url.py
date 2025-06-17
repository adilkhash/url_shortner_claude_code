from datetime import datetime
from typing import Optional


class URLModel:
    def __init__(
        self,
        id: Optional[int] = None,
        original_url: str = "",
        short_code: str = "",
        created_at: Optional[datetime] = None,
        click_count: int = 0,
        expires_at: Optional[datetime] = None,
        is_active: bool = True
    ):
        self.id = id
        self.original_url = original_url
        self.short_code = short_code
        self.created_at = created_at or datetime.utcnow()
        self.click_count = click_count
        self.expires_at = expires_at
        self.is_active = is_active

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "original_url": self.original_url,
            "short_code": self.short_code,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "click_count": self.click_count,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_active": self.is_active
        }

    @classmethod
    def from_dict(cls, data: dict) -> "URLModel":
        return cls(
            id=data.get("id"),
            original_url=data.get("original_url", ""),
            short_code=data.get("short_code", ""),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            click_count=data.get("click_count", 0),
            expires_at=datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None,
            is_active=data.get("is_active", True)
        )