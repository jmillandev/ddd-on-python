from dataclasses import asdict, dataclass

from sqlalchemy import UUID, Column, DateTime, func
from sqlalchemy.orm import as_declarative



@as_declarative()
class Base:
    id = Column(UUID, primary_key=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False
    )

    @classmethod
    def from_entity(cls, entity: dataclass) -> 'Base':
        data = asdict(entity)
        for key in data:
            data[key] = data[key].primitive
        return cls(**data)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
