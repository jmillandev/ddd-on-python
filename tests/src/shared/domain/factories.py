from src.planner.shared.application.mappers import dict_to_entity
from src.planner.shared.domain.aggregates import AggregateRoot

from dataclasses import asdict
from abc import ABCMeta

class AggregateRootFactory(metaclass=ABCMeta):
    _AgregateClass: type[AggregateRoot]

    @classmethod
    def build(cls, **kwargs) -> AggregateRoot:
        return dict_to_entity(cls(**kwargs).to_dict(), cls._AgregateClass)

    def to_dict(self) -> dict:
        return asdict(self)
