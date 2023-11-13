from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from db.base_repository import BaseRepository
from tests.conftest import database

fake = Faker()


class Factory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        session = await anext(database())
        return await BaseRepository(session).create(obj)
