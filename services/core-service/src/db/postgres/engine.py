from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from ...config.settings import settings

DB_URI = settings.get_pg_url

base = declarative_base()

engine = create_async_engine(
    DB_URI,
    echo=False,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

async def db_heath_check() -> bool:
    async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            await session.execute(text("SELECT pg_sleep(0.5)"))
            return True

async def initialize_table():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)



