from dataclasses import dataclass

from src.planner.movements.domain.aggregate import Movement
from src.planner.shared.domain.accounts import AccountId


@dataclass
class TransferMovement(Movement):
    from_account_id: AccountId
    to_account_id: AccountId
