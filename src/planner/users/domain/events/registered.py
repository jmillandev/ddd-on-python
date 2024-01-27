from src.shared.domain.bus.event.domain_event import DomainEvent, DomainEventName
from dataclasses import dataclass


@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    email: str
    pronoun: str
    name: str
    last_name: str


    @staticmethod
    def event_name() -> DomainEventName:
        'user.registered'

    def payload(self) -> dict:
        {
            "email": self.email,
            "pronoun": self.pronoun,
            "name": self.name,
            "last_name": self.last_name   
        }
