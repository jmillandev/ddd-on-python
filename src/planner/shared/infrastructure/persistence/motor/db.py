from motor.core import AgnosticClient, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from src.planner.shared.config import settings


def database(db_name: str = settings.MONGO_DB) -> AgnosticDatabase:
    client: AgnosticClient = AsyncIOMotorClient(str(settings.MONGO_DETAILS))

    return client[db_name]
