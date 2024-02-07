from dataclasses import dataclass

from src.planner.movements.domain.aggregate import Movement
from src.planner.shared.domain.accounts import AccountId


@dataclass
class IncomeMovement(Movement):
    account_id: AccountId
