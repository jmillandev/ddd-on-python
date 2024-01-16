import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.planner.users.infrastructure.repositories.sqlalchemy import (
    SqlAlcheamyUserRepository,
)
from tests.src.planner.users.factories import UserFactory

pytestmark = pytest.mark.anyio


class TestSqlAlchemyUserRepository:
    async def test_should_create_a_user(self, sqlalchemy_session: AsyncSession):
        repository = SqlAlcheamyUserRepository(sqlalchemy_session)
        user = UserFactory.build()

        await repository.create(user)

    async def test_should_return_a_user_by_id(self, sqlalchemy_session: AsyncSession):
        repository = SqlAlcheamyUserRepository(sqlalchemy_session)
        user = UserFactory.build()

        await repository.create(user)

        assert user == await repository.search(user.id)

    async def test_should_not_return_a_non_existing_user(
        self, sqlalchemy_session: AsyncSession
    ):
        repository = SqlAlcheamyUserRepository(sqlalchemy_session)
        user = UserFactory.build()

        assert await repository.search(user.id) is None
        assert await repository.search_by_email(user.email) is None

    async def test_should_return_a_user_by_email(
        self, sqlalchemy_session: AsyncSession
    ):
        repository = SqlAlcheamyUserRepository(sqlalchemy_session)
        user = UserFactory.build()

        await repository.create(user)
        perssisted_user = await repository.search_by_email(user.email)
        assert user == perssisted_user
