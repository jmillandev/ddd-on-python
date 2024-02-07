import pytest
from kink import di
from sqlalchemy.ext.asyncio import AsyncSession

from src.planner.accounts.infrastructure.repositories.sqlalchemy import (
    SqlAlchemyAccountRepository
)
from src.planner.expenses.infrastructure.repositories.sqlalchemy import SqlAlchemyExpenseRepository
from src.planner.expenses.domain.repository import ExpenseRepository
from src.planner.users.domain.repository import UserRepository
from src.planner.accounts.domain.repository import AccountRepository
from tests.src.planner.shared.factories.accounts import AccountFactory
from tests.src.planner.users.factories import UserFactory
from tests.src.planner.expenses.factories import ExpenseFactory


pytestmark = pytest.mark.anyio


class TestSqlAlchemyExpenseRepository:
    def setup_method(self):
        self.user = UserFactory.build()
        self.account = AccountFactory.build(owner_id=self.user.id.primitive)
        self.expense = ExpenseFactory.build(account_id=self.account.id.primitive)
    
    def test_should_be_a_valid_repository(self):
        assert issubclass(SqlAlchemyExpenseRepository, ExpenseRepository)

    async def test_should_create_a_account(self, sqlalchemy_session: AsyncSession):
        repository = SqlAlchemyExpenseRepository(sqlalchemy_session)
        await di[UserRepository].create(self.user)  # type:ignore [type-abstract]
        await di[AccountRepository].create(self.account)  # type:ignore [type-abstract]

        await repository.save(self.expense)

    async def test_should_not_return_a_non_existing_expense(
        self, sqlalchemy_session: AsyncSession
    ):
        repository = SqlAlchemyExpenseRepository(sqlalchemy_session)

        assert (
            await repository.search(self.expense.id)
            is None
        )

    async def test_should_return_an_expense_by_id(
        self, sqlalchemy_session: AsyncSession
    ):
        repository = SqlAlchemyExpenseRepository(sqlalchemy_session)
        await di[UserRepository].create(self.user)  # type:ignore [type-abstract]
        await di[AccountRepository].create(self.account)  # type:ignore [type-abstract]

        await repository.save(self.expense)
        perssisted_expense = await repository.search(self.expense.id)
        assert self.expense == perssisted_expense


    @pytest.mark.skip(reason="TODO: Return all user expenses.")
    async def test_should_return_all_user_expenses(
        self, sqlalchemy_session: AsyncSession
    ):
        ...
