from fastapi import FastAPI
from contextlib import asynccontextmanager
from ..config.settings import settings
# from ..config.logger import get_logger, configure_sql_logs
from ..db.postgres.engine import db_heath_check, engine, initialize_table
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):

    # configure_sql_logs()
    await initialize_table()
    try:
        await db_heath_check()
    except Exception as e:
        raise e
    yield
    await engine.dispose()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        lifespan=lifespan,
    )
    app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"])

    from ..api.v1.api_router import api_router
    app.include_router(api_router)

    return app

app = create_app()