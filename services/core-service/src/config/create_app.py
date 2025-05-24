from fastapi import FastAPI
from contextlib import asynccontextmanager
from ..config.settings import settings
from ..config.logger import get_logger
from ..db.postgres.engine import db_heath_check, engine


log = get_logger("core")

@asynccontextmanager
async def lifespan(app: FastAPI):

    log.info("Starting application")
    try:
        await db_heath_check()
        log.info("Database health check successful")
    except Exception as e:
        log.error(f"Database health check failed: {e}")
        raise e

    yield

    log.info("Shutting down application")
    await engine.dispose()
    log.info("Application shutdown complete")

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        lifespan=lifespan,
    )
    from ..middlewares.http_logging import LoggingMiddleware
    app.add_middleware(LoggingMiddleware)
    from ..api.v1.api_router import api_router
    app.include_router(api_router)

    log.info("FastAPI application created successfully")
    return app

app = create_app()