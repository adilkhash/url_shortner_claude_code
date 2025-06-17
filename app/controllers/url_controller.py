from typing import Annotated
from litestar import Controller, post, get, Request, Response
from litestar.status_codes import HTTP_201_CREATED, HTTP_301_MOVED_PERMANENTLY, HTTP_404_NOT_FOUND
from litestar.exceptions import NotFoundException, ValidationException
from app.schemas.url import CreateURLRequest, URLResponse, URLStatsResponse, CreateURLDTO, URLResponseDTO, URLStatsDTO
from app.services.url_service import URLService
from app.exceptions import URLNotFoundException, DuplicateShortCodeException, InvalidURLException, ExpiredURLException
from app.validators import URLValidator


class URLController(Controller):
    path = "/api/v1/urls"
    
    def __init__(self, url_service: URLService):
        self.url_service = url_service

    @post("/", dto=CreateURLDTO, return_dto=URLResponseDTO, status_code=HTTP_201_CREATED)
    async def create_short_url(self, data: CreateURLRequest, request: Request) -> URLResponse:
        original_url = str(data.original_url)
        
        if not URLValidator.is_valid_url(original_url):
            raise InvalidURLException(detail="Invalid URL format")
        
        if not URLValidator.validate_url_length(original_url):
            raise InvalidURLException(detail="URL is too long")
        
        if data.custom_code and not URLValidator.is_valid_short_code(data.custom_code):
            raise InvalidURLException(detail="Invalid custom short code format")
        
        try:
            url = self.url_service.create_url(
                original_url=original_url,
                custom_code=data.custom_code,
                expires_at=data.expires_at
            )
            
            base_url = f"{request.url.scheme}://{request.url.netloc}"
            short_url = f"{base_url}/{url.short_code}"
            
            return URLResponse(
                id=url.id,
                original_url=url.original_url,
                short_code=url.short_code,
                short_url=short_url,
                created_at=url.created_at,
                click_count=url.click_count,
                expires_at=url.expires_at,
                is_active=url.is_active
            )
        except ValueError as e:
            if "already exists" in str(e):
                raise DuplicateShortCodeException(detail=str(e))
            raise InvalidURLException(detail=str(e))

    @get("/{short_code:str}/stats", return_dto=URLStatsDTO)
    async def get_url_stats(self, short_code: str, request: Request) -> URLStatsResponse:
        if not URLValidator.is_valid_short_code(short_code):
            raise InvalidURLException(detail="Invalid short code format")
            
        url = self.url_service.get_url_by_short_code(short_code)
        if not url:
            raise URLNotFoundException(detail=f"URL with short code '{short_code}' not found")
        
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        short_url = f"{base_url}/{url.short_code}"
        
        return URLStatsResponse(
            id=url.id,
            original_url=url.original_url,
            short_code=url.short_code,
            short_url=short_url,
            created_at=url.created_at,
            click_count=url.click_count,
            expires_at=url.expires_at,
            is_active=url.is_active
        )


class RedirectController(Controller):
    path = "/"
    
    def __init__(self, url_service: URLService):
        self.url_service = url_service

    @get("/{short_code:str}")
    async def redirect_to_original(self, short_code: str) -> Response:
        if not URLValidator.is_valid_short_code(short_code):
            raise URLNotFoundException(detail="Invalid short code format")
            
        url = self.url_service.get_url_by_short_code(short_code)
        
        if not url:
            raise URLNotFoundException(detail="URL not found")
        
        if not url.is_active:
            raise URLNotFoundException(detail="URL is no longer active")
        
        if self.url_service.is_url_expired(url):
            raise ExpiredURLException(detail="URL has expired")
        
        self.url_service.increment_click_count(url.id)
        
        return Response(
            content="",
            status_code=HTTP_301_MOVED_PERMANENTLY,
            headers={"Location": url.original_url}
        )