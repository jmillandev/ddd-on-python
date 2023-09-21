from faker import Faker

from factory.alchemy import SQLAlchemyModelFactory
from tests.conftest import database
from db.base_repository import BaseRepository

fake = Faker()


class Factory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        session = await anext(database())
        return await BaseRepository(session).create(obj)
