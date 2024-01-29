from abc import ABCMeta, abstractmethod
from dataclasses import dataclass as _dataclass
from typing import List, dataclass_transform

from src.shared.domain.bus.event.domain_event import DomainEvent


@dataclass_transform()
def aggregate_dataclass(cls):
    """Decorator that applies dataclass_transform to all fields of the class"""

    def wrap(cls):
        return _dataclass(cls, eq=False, repr=False)

    return wrap(cls)


class AggregateRoot(metaclass=ABCMeta):
    def __post_init__(self, *args, **kwargs):
        """Dataclass Method used instead __init__"""
        self._flush_events()

    def pull_domain_events(self) -> List[DomainEvent]:
        events = self._recorded_events
        self._flush_events()
        return events

    def _record_event(self, event: DomainEvent):
        self._recorded_events.append(event)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}('{(self)}')>"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        return self.id == o.id  # type: ignore[attr-defined]

    def _flush_events(self) -> None:
        self._recorded_events: List[DomainEvent] = []

    @abstractmethod
    def __str__(self) -> str:
        ...
