from dataclasses import dataclass

from src.shared.domain.bus.event.domain_event import DomainEvent


@dataclass(frozen=True)
class IncomeMovementAdded(DomainEvent):
    date: str
    amount: int
    account_id: str

    @staticmethod
    def event_name() -> str:
        return "planner.movements.income_added"

    def payload(self) -> dict:
        return {"date": self.date, "amount": self.amount, "account_id": self.account_id}
