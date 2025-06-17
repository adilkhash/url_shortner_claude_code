from datetime import datetime
from typing import Optional
from litestar.contrib.pydantic import PydanticDTO
from pydantic import BaseModel, HttpUrl, Field


class CreateURLRequest(BaseModel):
    original_url: HttpUrl
    custom_code: Optional[str] = Field(None, min_length=3, max_length=20, pattern="^[a-zA-Z0-9_-]+$")
    expires_at: Optional[datetime] = None


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    created_at: datetime
    click_count: int
    expires_at: Optional[datetime] = None
    is_active: bool


class URLStatsResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    created_at: datetime
    click_count: int
    expires_at: Optional[datetime] = None
    is_active: bool


CreateURLDTO = PydanticDTO[CreateURLRequest]
URLResponseDTO = PydanticDTO[URLResponse]
URLStatsDTO = PydanticDTO[URLStatsResponse]