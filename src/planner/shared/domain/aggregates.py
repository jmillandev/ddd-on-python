from abc import ABCMeta, abstractmethod
from typing import List
from src.shared.domain.bus.event.domain_event import DomainEvent
from dataclasses import dataclass


class AggregateRoot(metaclass=ABCMeta):

    def __init_subclass__(cls, **kwargs):
        """Apply dataclass decorator to all of subclasses 
        """  
        return dataclass(cls, eq=False, repr=False)

    def __post_init__(self, *args, **kwargs):
        """Dataclass Method used instead __init__
        """
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
        return self.id == o.id

    def _flush_events(self) -> None:
        self._recorded_events: List[DomainEvent] = []

    @abstractmethod
    def __str__(self) -> str:
        ...
