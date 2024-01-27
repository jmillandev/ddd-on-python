from src.shared.domain.bus.event.event_bus import EventBus
from src.shared.infrastructure.bus.event.in_memory.event_bus import InMemoryEventBus


def start_event_bus()-> EventBus:
    # TODO: Look for subscribers in the project
    subscribers = set()
    return InMemoryEventBus(subscribers)
