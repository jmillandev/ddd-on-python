from typing import Set

from src.shared.domain.bus.event.domain_event_susbcriber import DomainEventSubscriber
from src.shared.domain.bus.event.event_bus import EventBus
from src.shared.infrastructure.bus.event.in_memory.event_bus import InMemoryEventBus


def start_event_bus() -> EventBus:
    # TODO: Look for subscribers in the project
    subscribers: Set[DomainEventSubscriber] = set()
    return InMemoryEventBus(subscribers)
