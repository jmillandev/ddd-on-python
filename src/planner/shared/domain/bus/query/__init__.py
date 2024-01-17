from dataclasses import dataclass
from typing import Optional, Protocol, TypeVar, runtime_checkable, ClassVar, Dict

@runtime_checkable
class Query(Protocol):
    __dataclass_fields__: ClassVar[Dict] 

@runtime_checkable
class QueryResponse(Protocol):
    __dataclass_fields__: ClassVar[Dict] 


@runtime_checkable
class QueryBus(Protocol):
    def ask(self, query: Query) -> Optional[QueryResponse]:
        ...
