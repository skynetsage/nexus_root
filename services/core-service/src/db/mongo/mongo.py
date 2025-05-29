from motor.motor_asyncio import AsyncIOMotorClient
from ...config.settings import settings # adjust path as needed

client = AsyncIOMotorClient(settings.MONGO_URI)
mongodb = client[settings.MONGO_DB]