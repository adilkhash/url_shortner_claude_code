from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR


class URLNotFoundException(HTTPException):
    status_code = HTTP_404_NOT_FOUND
    detail = "URL not found"


class DuplicateShortCodeException(HTTPException):
    status_code = HTTP_409_CONFLICT
    detail = "Short code already exists"


class InvalidURLException(HTTPException):
    status_code = HTTP_400_BAD_REQUEST
    detail = "Invalid URL provided"


class ExpiredURLException(HTTPException):
    status_code = HTTP_404_NOT_FOUND
    detail = "URL has expired"


class DatabaseException(HTTPException):
    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Database operation failed"


class ShortCodeGenerationException(HTTPException):
    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to generate unique short code"