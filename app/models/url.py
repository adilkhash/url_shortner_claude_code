from datetime import datetime, timezone
from typing import Optional, Self
from dateutil.parser import parse
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class URLModel(Base):
    __tablename__ = 'urls'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
    click_count = Column(Integer, default=0, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __init__(
        self,
        original_url: str = "",
        short_code: str = "",
        created_at: Optional[datetime] = None,
        click_count: int = 0,
        expires_at: Optional[datetime] = None,
        is_active: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.original_url = original_url
        self.short_code = short_code
        if created_at:
            self.created_at = created_at
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
    def from_dict(cls, data: dict) -> Self:
        created_at = data.get("created_at")
        if created_at and isinstance(created_at, str):
            created_at = parse(created_at)
        elif not isinstance(created_at, datetime):
            created_at = None

        expires_at = data.get("expires_at")
        if expires_at and isinstance(expires_at, str):
            expires_at = parse(expires_at)
        elif not isinstance(expires_at, datetime):
            expires_at = None

        return cls(
            id=data.get("id"),
            original_url=data.get("original_url", ""),
            short_code=data.get("short_code", ""),
            created_at=created_at,
            click_count=data.get("click_count", 0),
            expires_at=expires_at,
            is_active=data.get("is_active", True)
        )
