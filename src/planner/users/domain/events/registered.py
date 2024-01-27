from dataclasses import dataclass

from src.shared.domain.bus.event.domain_event import DomainEvent


@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    email: str
    pronoun: str
    name: str
    last_name: str

    @staticmethod
    def event_name() -> str:
        return "user.registered"

    def payload(self) -> dict:
        return {
            "email": self.email,
            "pronoun": self.pronoun,
            "name": self.name,
            "last_name": self.last_name,
        }
