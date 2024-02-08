from dataclasses import dataclass

from src.shared.domain.bus.event.domain_event import DomainEvent


@dataclass(frozen=True)
class AccountBalanceUpdated(DomainEvent):
    owner_id: str
    name: str
    currency: str
    balance: int

    @staticmethod
    def event_name() -> str:
        return "planner.account.balance_updated"

    def payload(self) -> dict:
        return {
            "owner_id": self.owner_id,
            "currency": self.currency,
            "name": self.name,
            "balance": self.balance,
        }
