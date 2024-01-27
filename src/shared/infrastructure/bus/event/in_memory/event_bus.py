from typing import Dict, Sequence, Set, Awaitable, Callable
from src.shared.domain.bus.event.domain_event import DomainEvent, DomainEventName
from src.shared.domain.bus.event.domain_event_susbcriber import DomainEventSubscriber
from asyncio import gather
from collections import defaultdict


class InMemoryEventBus:
    _subscriptions: Dict[DomainEventName, Set[Callable[[], Awaitable[None]]]]

    def __init__(self, subscribers: Sequence[DomainEventSubscriber]) -> None:
        self._subscriptions = defaultdict(set)
        for subscriber in subscribers:
            for event_name in subscriber.subscribed_to():
                self._subscriptions[event_name].add(subscriber)

    async def publish(self, *events: DomainEvent) -> None:
        coros = set()
        for event in events:
            for subscriber in self._subscriptions[event.event_name]:
                coros.add(subscriber(event))
        
        await gather(*coros)
