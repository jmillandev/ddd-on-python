from dataclasses import asdict, dataclass

from sqlalchemy import UUID, Column, DateTime, func
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    @classmethod
    def from_entity(cls, entity: dataclass) -> "Base":
        data = asdict(entity)
        for key in data:
            data[key] = data[key].primitive
        return cls(**data)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
