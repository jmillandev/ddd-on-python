from kink import inject

from src.planner.expenses.application.auth import ExpenseAuthorizationService
from src.planner.expenses.domain.entity import Expense
from src.planner.expenses.domain.repository import ExpenseRepository
from src.planner.expenses.domain.value_objects import (
    ExpenseAmount,
    ExpenseDate,
    ExpenseId,
)
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.users import UserId
from src.shared.domain.bus.event.event_bus import EventBus


@inject
class ExpenseAdder:
    def __init__(
        self,
        repository: ExpenseRepository,
        event_bus: EventBus,
        auth_service: ExpenseAuthorizationService,
    ):
        self._repository = repository
        self._event_bus = event_bus
        self._auth_service = auth_service

    async def __call__(
        self,
        id: ExpenseId,
        amount: ExpenseAmount,
        date: ExpenseDate,
        account_id: AccountId,
        user_id: UserId,
    ) -> None:
        await self._auth_service.ensure_user_is_account_owner(account_id, user_id)
        expense = Expense.add(id, amount, account_id, date)
        await self._repository.save(expense)
        await self._event_bus.publish(*expense.pull_domain_events())
