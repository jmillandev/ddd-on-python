from dataclasses import asdict

from sqlalchemy.orm import as_declarative

from src.planner.shared.domain.aggregates import RootAggregate


@as_declarative()
class Base:
    @classmethod
    def from_entity(cls, entity: RootAggregate) -> "Base":
        data = asdict(entity)
        for key in data:
            data[key] = data[key].primitive
        return cls(**data)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
