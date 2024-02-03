from dataclasses import asdict
from typing import Self

from sqlalchemy.orm import as_declarative

from src.planner.shared.domain.aggregates import AggregateRoot


@as_declarative()
class Base:
    @classmethod
    def from_entity(cls, entity: AggregateRoot) -> Self:
        data = asdict(entity)  # type: ignore[call-overload]
        for key in data:
            data[key] = data[key].value
        return cls(**data)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
