from kink import inject

from src.planner.movements.domain.value_objects import (
    MovementAmount,
    MovementDate,
    MovementId,
)
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.users import UserId

from .adder import IncomeMovementAdder
from .command import AddIncomeMovementCommand


@inject
class AddIncomeMovementCommandHandler:
    def __init__(self, use_case: IncomeMovementAdder) -> None:
        self.use_case = use_case

    async def __call__(self, command: AddIncomeMovementCommand) -> None:
        await self.use_case(
            id=MovementId(command.id),
            amount=MovementAmount(command.amount),
            account_id=AccountId(command.account_id),
            date=MovementDate(command.date),
            user_id=UserId(command.user_id),
        )
