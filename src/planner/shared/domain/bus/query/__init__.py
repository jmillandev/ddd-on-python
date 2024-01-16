from dataclasses import dataclass
from typing import Optional, Protocol, TypeVar, runtime_checkable

Query = TypeVar("Query", bound=dataclass)
QueryResponse = TypeVar("QueryResponse", bound=dict)


@runtime_checkable
class QueryBus(Protocol):
    def ask(self, query: Query) -> Optional[QueryResponse]:
        ...
