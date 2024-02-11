from kink import inject

from src.planner.movements.application.auth import MovementAuthorizationService
from src.planner.movements.domain.repository import MovementRepository
from src.planner.movements.domain.transfers.aggregate import TransferMovement
from src.planner.movements.domain.value_objects import (
    MovementAmount,
    MovementDate,
    MovementId,
)
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.users import UserId
from src.shared.domain.bus.event.event_bus import EventBus


@inject(use_factory=True)
class TransferMovementAdder:
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
        origin_id: AccountId,
        destination_id: AccountId,
        user_id: UserId,
    ) -> None:
        # TODO: Use gather to improve performance - https://github.com/sqlalchemy/sqlalchemy/discussions/9312  # noqa: E501
        await self._auth_service.ensure_user_is_account_owner(origin_id, user_id)
        await self._auth_service.ensure_user_is_account_owner(destination_id, user_id)
        expense = TransferMovement.add(id, amount, origin_id, destination_id, date)
        await self._repository.save(expense)
        await self._event_bus.publish(*expense.pull_domain_events())
