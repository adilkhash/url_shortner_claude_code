import re
from urllib.parse import urlparse
from typing import Optional


class URLValidator:
    @staticmethod
    def is_valid_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
        except Exception:
            return False

    @staticmethod
    def is_valid_short_code(short_code: str) -> bool:
        if not short_code or len(short_code) < 3 or len(short_code) > 20:
            return False
        
        pattern = r'^[a-zA-Z0-9_-]+$'
        return bool(re.match(pattern, short_code))

    @staticmethod
    def sanitize_url(url: str) -> str:
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

    @staticmethod
    def validate_url_length(url: str, max_length: int = 2048) -> bool:
        return len(url) <= max_length


class ValidationError(Exception):
    def __init__(self, message: str, field: Optional[str] = None):
        self.message = message
        self.field = field
        super().__init__(self.message)