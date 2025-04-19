from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import  text, event
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.logger import get_logger

DB_URL = settings.postgres_uri
log = get_logger("postgres")

engine = create_async_engine(DB_URL, future=True, echo=True)
sync_engine = engine.sync_engine

@event.listens_for(sync_engine, "before_cursor_execute")
def log_sql(conn, cursor, statement, parameters, context, executemany):
    log.debug("SQL executed", {"statement": statement, "params": parameters})

@event.listens_for(sync_engine, "handle_error")
def log_sql_error(context):
    log.error("SQL error", {"statement": context.statement, "params": context.parameters}, exc_info=True)

AsyncSessionLocal = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def check_postgres_connection():
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text('SELECT 1'))
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False