from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

_mongo_client = None

def get_mongo_client():
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = AsyncIOMotorClient(settings.mongodb_uri)
    return _mongo_client

async def get_mongo_db():
    client = await get_mongo_client()
    db = client[settings.MONGO_DB]
    return db

async def check_mongo_connection():
    try:
        client = get_mongo_client()
        await client.admin.command('ping')
        return True
    except Exception as e:
        return False, str(e)