from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import  text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

DB_URL = settings.postgres_uri

engine = create_async_engine(DB_URL, future=True, echo=True)
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