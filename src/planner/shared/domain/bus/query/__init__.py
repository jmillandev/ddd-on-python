from typing import ClassVar, Dict, Optional, Protocol, runtime_checkable


@runtime_checkable
class Query(Protocol):
    __dataclass_fields__: ClassVar[Dict]


@runtime_checkable
class QueryResponse(Protocol):
    __dataclass_fields__: ClassVar[Dict]


@runtime_checkable
class QueryBus(Protocol):
    async def ask(self, query: Query) -> Optional[QueryResponse]:
        ...
