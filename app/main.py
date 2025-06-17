from litestar import Litestar, Request, Response
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.config.cors import CORSConfig
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.logging import LoggingConfig

from app.controllers.url_controller import URLController, RedirectController
from app.services.url_service import URLService
from app.repositories.url_repository import URLRepository
from app.config.database import create_database_connection, run_migrations
from app.config.settings import settings


def provide_url_service() -> URLService:
    db_connection = create_database_connection()
    repository = URLRepository(db_connection)
    return URLService(repository)


async def exception_handler(request: Request, exc: Exception) -> Response:
    if isinstance(exc, HTTPException):
        return Response(
            content={"error": exc.detail, "status_code": exc.status_code},
            status_code=exc.status_code,
            media_type="application/json"
        )
    
    return Response(
        content={"error": "Internal server error", "status_code": HTTP_500_INTERNAL_SERVER_ERROR},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        media_type="application/json"
    )


def create_app() -> Litestar:
    cors_config = CORSConfig(
        allow_origins=settings.allowed_origins if settings.allowed_origins else ["*"],
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        allow_credentials=True
    )
    
    logging_config = LoggingConfig(
        root={"level": "INFO" if not settings.debug else "DEBUG", "handlers": ["console"]},
        formatters={
            "standard": {"format": "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"}
        }
    )

    app = Litestar(
        route_handlers=[URLController, RedirectController],
        dependencies={"url_service": Provide(provide_url_service)},
        cors_config=cors_config,
        logging_config=logging_config,
        debug=settings.debug,
        exception_handlers={Exception: exception_handler},
    )
    
    return app


async def lifespan_startup():
    db_connection = create_database_connection()
    try:
        run_migrations(db_connection)
        print("Database migrations completed successfully")
    except Exception as e:
        print(f"Error running migrations: {e}")
        raise
    finally:
        db_connection.close()


async def lifespan_shutdown():
    print("Application shutting down...")


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )
