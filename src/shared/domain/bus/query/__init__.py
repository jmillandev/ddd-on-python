from typing import Protocol, runtime_checkable, TypeVar, Optional, Generic
from dataclasses import dataclass

Query = TypeVar("Query", bound=dataclass)
QueryResponse = TypeVar("QueryResponse", bound=dict)


@runtime_checkable
class QueryBus(Protocol):
    def ask(self, query: Query) -> Optional[QueryResponse]:
        ...
