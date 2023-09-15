import pymongo
from pymongo.database import Database

from src.infrastructure.config_reader import settings


def mongo_connection() -> Database:
    """MongoDB connector."""
    client = pymongo.MongoClient(
        username=settings.mongo.username,
        password=settings.mongo.password,
        host=settings.mongo.host,
        port=settings.mongo.port,
    )

    return client.bachata_warehouse
