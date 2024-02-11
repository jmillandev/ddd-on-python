from kink import inject

from src.planner.movements.application.auth import MovementAuthorizationService
from src.planner.movements.domain.incomes.aggregate import IncomeMovement
from src.planner.movements.domain.repository import MovementRepository
from src.planner.movements.domain.value_objects import (
    MovementAmount,
    MovementDate,
    MovementId,
)
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.users import UserId
from src.shared.domain.bus.event.event_bus import EventBus


@inject
class IncomeMovementAdder:
    def __init__(
        self,
        repository: MovementRepository,
        event_bus: EventBus,
        auth_service: MovementAuthorizationService,
    ):
        self._repository = repository
        self._event_bus = event_bus
        self._auth_service = auth_service

    async def __call__(
        self,
        id: MovementId,
        amount: MovementAmount,
        date: MovementDate,
        account_id: AccountId,
        user_id: UserId,
    ) -> None:
        await self._auth_service.ensure_user_is_account_owner(account_id, user_id)
        expense = IncomeMovement.add(id, amount, account_id, date)
        await self._repository.save(expense)
        await self._event_bus.publish(*expense.pull_domain_events())
