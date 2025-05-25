from fastapi import FastAPI
from contextlib import asynccontextmanager
from ..config.settings import settings
from ..config.logger import get_logger, configure_sql_logs
from ..db.postgres.engine import db_heath_check, engine, initialize_table


log = get_logger("core")

@asynccontextmanager
async def lifespan(app: FastAPI):

    configure_sql_logs()
    log.info("Starting application")
    await initialize_table()
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
    from ..middlewares.http_logging import HTTPLoggingMiddleware
    app.add_middleware(HTTPLoggingMiddleware)
    from ..api.v1.api_router import api_router
    app.include_router(api_router)

    log.info("FastAPI application created successfully")
    return app

app = create_app()