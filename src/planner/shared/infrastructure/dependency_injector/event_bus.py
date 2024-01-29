from importlib import import_module
from pathlib import Path
from typing import Set

from src.shared.domain.bus.event.domain_event_susbcriber import DomainEventSubscriber
from src.shared.domain.bus.event.event_bus import EventBus
from src.shared.infrastructure.bus.event.in_memory.event_bus import InMemoryEventBus


def start_event_bus() -> EventBus:
    for module_name in Path(".").glob("src/**/application/*/subscribers"):
        import_module(str(module_name).replace("/", "."))

    subscribers: Set[type[DomainEventSubscriber]] = set(
        DomainEventSubscriber.__subclasses__()
    )
    return InMemoryEventBus(subscribers)
