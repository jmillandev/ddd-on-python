from asyncio import gather
from collections import defaultdict
from typing import Dict, Set

from kink import inject

from src.shared.domain.bus.event.domain_event import DomainEvent
from src.shared.domain.bus.event.domain_event_susbcriber import DomainEventSubscriber
from src.shared.domain.bus.event.event_bus import EventBus


@inject(alias=EventBus)
class InMemoryEventBus:
    _subscriptions: Dict[str, Set[type[DomainEventSubscriber]]]

    def __init__(self, subscribers: Set[type[DomainEventSubscriber]]) -> None:
        self._subscriptions = defaultdict(set)
        for subscriber in subscribers:
            self._subscriptions[subscriber.subscribed_to().event_name()].add(subscriber)

    async def publish(self, *events: DomainEvent) -> None:
        coros = set()
        for event in events:
            for subscriber in self._subscriptions[event.event_name()]:
                coros.add(subscriber()(event))

        await gather(*coros)
