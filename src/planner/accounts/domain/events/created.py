from dataclasses import dataclass

from src.shared.domain.bus.event.domain_event import DomainEvent


@dataclass(frozen=True)
class AccountCreated(DomainEvent):
    user_id: str
    name: str
    currency: str
    balance: int

    @staticmethod
    def event_name() -> str:
        return "planner.account.created"

    def payload(self) -> dict:
        return {
            "user_id": self.user_id,
            "currency": self.currency,
            "name": self.name,
            "balance": self.balance,
        }
    