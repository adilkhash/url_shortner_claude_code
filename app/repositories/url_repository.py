from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.url import URLModel


class URLRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def create(self, url: URLModel) -> URLModel:
        session = self.db.get_session()
        try:
            session.add(url)
            session.commit()
            session.refresh(url)
            return url
        except Exception as e:
            session.rollback()
            raise Exception(f"Failed to create URL: {str(e)}")

    def get_by_short_code(self, short_code: str) -> Optional[URLModel]:
        session = self.db.get_session()
        return session.query(URLModel).filter(
            URLModel.short_code == short_code,
            URLModel.is_active == True
        ).first()

    def get_by_id(self, url_id: int) -> Optional[URLModel]:
        session = self.db.get_session()
        return session.query(URLModel).filter(URLModel.id == url_id).first()

    def increment_click_count(self, url_id: int) -> Optional[URLModel]:
        session = self.db.get_session()
        try:
            url = session.query(URLModel).filter(URLModel.id == url_id).first()
            if url:
                url.click_count += 1
                session.commit()
                return url
            return None
        except Exception as e:
            session.rollback()
            raise Exception(f"Failed to increment click count: {str(e)}")

    def deactivate_url(self, url_id: int) -> bool:
        session = self.db.get_session()
        try:
            url = session.query(URLModel).filter(URLModel.id == url_id).first()
            if url:
                url.is_active = False
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise Exception(f"Failed to deactivate URL: {str(e)}")

    def cleanup_expired_urls(self) -> int:
        session = self.db.get_session()
        try:
            affected_rows = session.query(URLModel).filter(
                URLModel.expires_at < datetime.utcnow(),
                URLModel.is_active == True
            ).update({URLModel.is_active: False})
            session.commit()
            return affected_rows
        except Exception as e:
            session.rollback()
            raise Exception(f"Failed to cleanup expired URLs: {str(e)}")