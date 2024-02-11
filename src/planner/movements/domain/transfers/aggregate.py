from dataclasses import dataclass
from typing import Self

from src.planner.movements.domain.aggregate import Movement
from src.planner.movements.domain.value_objects.amount import MovementAmount
from src.planner.movements.domain.value_objects.date import MovementDate
from src.planner.movements.domain.value_objects.id import MovementId
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.movements.events import TransferMovementAdded


@dataclass
class TransferMovement(Movement):
    origin_id: AccountId
    destination_id: AccountId

    @classmethod
    def add(
        cls,
        id: MovementId,
        amount: MovementAmount,
        origin_id: AccountId,
        destination_id: AccountId,
        date: MovementDate,
    ) -> Self:
        transfer = cls(
            id=id,
            amount=amount,
            origin_id=origin_id,
            destination_id=destination_id,
            date=date,
        )
        transfer._record_event(
            TransferMovementAdded.make(
                transfer.id.primitive,
                date=transfer.date.primitive,
                amount=transfer.amount.primitive,
                origin_id=transfer.origin_id.primitive,
                destination_id=transfer.destination_id.primitive,
            )
        )
        return transfer
