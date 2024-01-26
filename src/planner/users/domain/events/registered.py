from src.shared.domain.bus.event.domain_event import DomainEvent


class UserRegistered(DomainEvent):
    email: str
    pronoun: str
    name: str
    last_name: str
