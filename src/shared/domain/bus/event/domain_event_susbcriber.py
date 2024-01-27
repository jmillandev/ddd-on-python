from typing import Protocol, runtime_checkable, Set
from .domain_event import DomainEvent, DomainEventName


@runtime_checkable
class DomainEventSubscriber(Protocol):

    async def __call__(self, domain_event: DomainEvent) -> None:
        ...

    @staticmethod
    def subscribed_to() -> Set[DomainEventName]:
        ...
