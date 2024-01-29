from typing import Protocol, Set, runtime_checkable

from .domain_event import DomainEvent


@runtime_checkable
class DomainEventSubscriber(Protocol):
    async def __call__(self, event: DomainEvent) -> None:
        ...

    @staticmethod
    def subscribed_to() -> Set[type[DomainEvent]]:
        ...
