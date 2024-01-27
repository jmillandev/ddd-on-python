from abc import ABCMeta, abstractmethod
from calendar import timegm
from dataclasses import dataclass
from time import gmtime
from typing import Optional, Union
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DomainEvent(metaclass=ABCMeta):
    aggregate_id: UUID
    event_id: UUID
    ocurrend_at: int

    @staticmethod
    @abstractmethod
    def event_name() -> str:
        ...

    @abstractmethod
    def payload(self) -> dict:
        ...

    @classmethod
    def make(
        cls,
        aggregate_id: UUID,
        event_id: Optional[UUID] = None,
        ocurrend_at: Optional[int] = None,
        **attrs: Union[str, int, bool]
    ) -> "DomainEvent":
        return cls(
            aggregate_id=aggregate_id,
            event_id=event_id or uuid4(),
            ocurrend_at=ocurrend_at or timegm(gmtime()),
            **attrs
        )
