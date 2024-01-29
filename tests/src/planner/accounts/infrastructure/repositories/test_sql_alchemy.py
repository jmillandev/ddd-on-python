import pytest
from kink import di
from sqlalchemy.ext.asyncio import AsyncSession

from src.planner.accounts.infrastructure.repositories.sqlalchemy import (
    SqlAlcheamyAccountRepository,
)
from src.planner.users.domain.repository import UserRepository
from tests.src.planner.accounts.factories import AccountFactory
from tests.src.planner.users.factories import UserFactory

pytestmark = pytest.mark.anyio


class TestSqlAlchemyAccountRepository:
    def setup_method(self):
        self.user = UserFactory.build()
        self.account = AccountFactory.build(user_id=self.user.id.primitive)

    async def test_should_create_a_account(self, sqlalchemy_session: AsyncSession):
        repository = SqlAlcheamyAccountRepository(sqlalchemy_session)
        await di[UserRepository].create(self.user)  # type:ignore [type-abstract]

        await repository.create(self.account)

    async def test_should_not_return_a_non_existing_user(
        self, sqlalchemy_session: AsyncSession
    ):
        repository = SqlAlcheamyAccountRepository(sqlalchemy_session)

        assert (
            await repository.search_by_name_and_user_id(
                self.account.name, self.account.user_id
            )
            is None
        )

    async def test_should_return_an_account_by_user_and_name(
        self, sqlalchemy_session: AsyncSession
    ):
        repository = SqlAlcheamyAccountRepository(sqlalchemy_session)
        await di[UserRepository].create(self.user)  # type:ignore [type-abstract]

        await repository.create(self.account)
        perssisted_account = await repository.search_by_name_and_user_id(
            self.account.name, self.account.user_id
        )
        assert self.account == perssisted_account
