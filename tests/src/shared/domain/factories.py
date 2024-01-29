from abc import ABCMeta
from dataclasses import asdict
from typing import Generic, TypeVar

from src.planner.shared.application.mappers import dict_to_entity
from src.planner.shared.domain.aggregates import AggregateRoot

Aggregate = TypeVar("Aggregate", bound=AggregateRoot)


class AggregateRootFactory(Generic[Aggregate], metaclass=ABCMeta):
    _AgregateClass: type[Aggregate]

    @classmethod
    def build(cls, **kwargs) -> Aggregate:
        return dict_to_entity(cls(**kwargs).to_dict(), cls._AgregateClass)

    def to_dict(self) -> dict:
        return asdict(self)  # type: ignore[call-overload]
