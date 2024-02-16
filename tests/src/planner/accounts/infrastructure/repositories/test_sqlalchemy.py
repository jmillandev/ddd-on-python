import pytest
from kink import di
from sqlalchemy.ext.asyncio import AsyncSession

from src.planner.accounts.domain.repository import AccountRepository
from src.planner.accounts.infrastructure.repositories.sqlalchemy import (
    SqlAlchemyAccountRepository,
)
from src.planner.users.domain.repository import UserRepository
from tests.src.planner.shared.factories.accounts import AccountFactory
from tests.src.planner.users.factories import UserFactory

pytestmark = pytest.mark.anyio


class TestSqlAlchemyAccountRepository:
    def setup_method(self):
        self.user = UserFactory.build()
        self.account = AccountFactory.build(owner_id=self.user.id.primitive)

    def test_should_be_a_valid_repository(self):
        assert issubclass(SqlAlchemyAccountRepository, AccountRepository)

    async def test_should_create_an_account(
        self, sqlalchemy_sessionmaker: type[AsyncSession]
    ):
        repository = SqlAlchemyAccountRepository(sqlalchemy_sessionmaker)
        await di[UserRepository].create(self.user)  # type:ignore [type-abstract]

        await repository.save(self.account)

    async def test_should_update_an_account(
        self, sqlalchemy_sessionmaker: type[AsyncSession]
    ):
        repository = SqlAlchemyAccountRepository(sqlalchemy_sessionmaker)
        await di[UserRepository].create(self.user)  # type:ignore [type-abstract]

        await repository.save(self.account)
        await repository.save(self.account)

    async def test_should_not_return_a_non_existing_account(
        self, sqlalchemy_sessionmaker: type[AsyncSession]
    ):
        repository = SqlAlchemyAccountRepository(sqlalchemy_sessionmaker)

        assert (
            await repository.search_by_name_and_owner_id(
                self.account.name, self.account.owner_id
            )
            is None
        )
        assert (
            await repository.search_by_id_and_owner_id(
                self.account.id, self.account.owner_id
            )
            is None
        )

    async def test_should_return_an_account_by_user_and_name(
        self, sqlalchemy_sessionmaker: type[AsyncSession]
    ):
        repository = SqlAlchemyAccountRepository(sqlalchemy_sessionmaker)
        await di[UserRepository].create(self.user)  # type:ignore [type-abstract]

        await repository.save(self.account)
        perssisted_account = await repository.search_by_name_and_owner_id(
            self.account.name, self.account.owner_id
        )
        assert self.account == perssisted_account

    async def test_should_return_an_account_by_id_and_owner_id(
        self, sqlalchemy_sessionmaker: type[AsyncSession]
    ):
        repository = SqlAlchemyAccountRepository(sqlalchemy_sessionmaker)
        await di[UserRepository].create(self.user)  # type:ignore [type-abstract]

        await repository.save(self.account)
        perssisted_account = await repository.search_by_id_and_owner_id(
            self.account.id, self.account.owner_id
        )
        assert self.account == perssisted_account
