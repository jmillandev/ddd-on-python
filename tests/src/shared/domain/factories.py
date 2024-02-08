from abc import ABCMeta
from dataclasses import asdict, field, dataclass
from typing import Generic, TypeVar

from faker import Faker

from src.planner.shared.application.mappers import dict_to_entity
from src.planner.shared.domain.aggregates import AggregateRoot
from src.shared.domain.bus.event.domain_event import DomainEvent

Aggregate = TypeVar("Aggregate", bound=AggregateRoot)
Event = TypeVar("Event", bound=DomainEvent)

fake = Faker()

class AggregateRootFactory(Generic[Aggregate], metaclass=ABCMeta):
    _AgregateClass: type[Aggregate]

    @classmethod
    def build(cls, **kwargs) -> Aggregate:
        return cls(**kwargs).aggregate()

    def aggregate(self) -> Aggregate:
        return dict_to_entity(self.to_dict(), self._AgregateClass)

    def to_dict(self) -> dict:
        return asdict(self)  # type: ignore[call-overload]    


@dataclass
class EventDomainFactory(Generic[Event], metaclass=ABCMeta):
    _EventClass: type[Event] = field(init=False)
    aggregate_id: str = field(default_factory=lambda: str(fake.uuid4()))
    event_id: str = field(default_factory=lambda: str(fake.uuid4()))
    ocurrend_at: int = field(default_factory=lambda: fake.unix_time())

    @classmethod
    def build(cls, **kwargs) -> Event:
        return cls(**kwargs).event()
    
    def event(self) -> Event:
        return self._EventClass(**self.to_dict())

    def to_dict(self) -> dict:
        dictionary = asdict(self)
        dictionary.pop("_EventClass")
        return dictionary
