from typing import Protocol, runtime_checkable
from .domain_event import DomainEvent


@runtime_checkable
class EventBus(Protocol):
    async def publish(self, *events: DomainEvent) -> None:
        ...
