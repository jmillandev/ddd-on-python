from dataclasses import dataclass

from src.shared.domain.bus.event.domain_event import DomainEvent


@dataclass(frozen=True)
class TransferMovementAdded(DomainEvent):
    date: str
    amount: int
    origin_id: str
    destination_id: str

    @staticmethod
    def event_name() -> str:
        return "planner.movements.transfer_added"

    def payload(self) -> dict:
        return {
            "date": self.date,
            "amount": self.amount,
            "origin_id": self.origin_id,
            "destination_id": self.destination_id,
        }
