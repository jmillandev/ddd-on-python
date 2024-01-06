import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.infrastructure.repositories import SqlAlcheamyUserRepository
from tests.src.users.factories import UserFactory

pytestmark = pytest.mark.anyio


class TestSqlAlchemyUserRepository:

    async def test_should_create_a_user(self, db_session: AsyncSession):
        repository = SqlAlcheamyUserRepository(db_session)
        user = UserFactory.build()

        await repository.create(user)


    async def test_should_return_a_user_by_id(self, db_session: AsyncSession):
        repository = SqlAlcheamyUserRepository(db_session)
        user = UserFactory.build()

        await repository.create(user)
        
        assert user == await repository.find(user.id)


    async def test_should_not_return_a_non_existing_user(self, db_session: AsyncSession):
        repository = SqlAlcheamyUserRepository(db_session)
        user = UserFactory.build()
        
        assert await repository.find(user.id) == None
        assert await repository.find_by_email(user.email) == None

    
    async def test_should_return_a_user_by_email(self, db_session: AsyncSession):
        repository = SqlAlcheamyUserRepository(db_session)
        user = UserFactory.build()

        await repository.create(user)
        
        assert user == await repository.find_by_email(user.email)
