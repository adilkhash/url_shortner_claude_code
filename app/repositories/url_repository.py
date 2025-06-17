from typing import Optional
from datetime import datetime
from app.models.url import URLModel


class URLRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def create(self, url: URLModel) -> URLModel:
        query = """
        INSERT INTO urls (original_url, short_code, created_at, expires_at, is_active)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, original_url, short_code, created_at, click_count, expires_at, is_active
        """
        
        cursor = self.db.cursor()
        cursor.execute(query, (
            url.original_url,
            url.short_code,
            url.created_at,
            url.expires_at,
            url.is_active
        ))
        
        row = cursor.fetchone()
        
        if row:
            cursor.close()
            self.db.commit()
            return URLModel.from_dict(row)

        cursor.close()
        
        raise Exception("Failed to create URL")

    def get_by_short_code(self, short_code: str) -> Optional[URLModel]:
        query = """
        SELECT id, original_url, short_code, created_at, click_count, expires_at, is_active
        FROM urls
        WHERE short_code = %s AND is_active = TRUE
        """
        
        cursor = self.db.cursor()
        cursor.execute(query, (short_code,))
        row = cursor.fetchone()
        cursor.close()
        
        if row:
            return URLModel.from_dict(row)

        return None

    def get_by_id(self, url_id: int) -> Optional[URLModel]:
        query = """
        SELECT id, original_url, short_code, created_at, click_count, expires_at, is_active
        FROM urls
        WHERE id = %s
        """
        
        cursor = self.db.cursor()
        cursor.execute(query, (url_id,))
        row = cursor.fetchone()
        cursor.close()
        
        if row:
            return URLModel.from_dict(row)
        
        return None

    def increment_click_count(self, url_id: int) -> Optional[URLModel]:
        query = """
        UPDATE urls
        SET click_count = click_count + 1
        WHERE id = %s
        RETURNING id, original_url, short_code, created_at, click_count, expires_at, is_active
        """
        
        cursor = self.db.cursor()
        cursor.execute(query, (url_id,))
        row = cursor.fetchone()
        
        if row:
            self.db.commit()
            cursor.close()
            return URLModel.from_dict(row)
        
        cursor.close()
        return None

    def deactivate_url(self, url_id: int) -> bool:
        query = """
        UPDATE urls
        SET is_active = FALSE
        WHERE id = %s
        """
        
        cursor = self.db.cursor()
        cursor.execute(query, (url_id,))
        affected_rows = cursor.rowcount
        self.db.commit()
        cursor.close()
        
        return affected_rows > 0

    def cleanup_expired_urls(self) -> int:
        query = """
        UPDATE urls
        SET is_active = FALSE
        WHERE expires_at < %s AND is_active = TRUE
        """
        
        cursor = self.db.cursor()
        cursor.execute(query, (datetime.utcnow(),))
        affected_rows = cursor.rowcount
        self.db.commit()
        cursor.close()
        
        return affected_rows