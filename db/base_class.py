from dataclasses import asdict
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, Integer, func
from sqlalchemy.orm import as_declarative, declared_attr



@as_declarative()
class Base:
    id = Column(UUID, primary_key=True, unique=True, default=uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False
    )

    @classmethod
    def from_entity(cls, entity):
        data = asdict(entity)
        for key in data:
            data[key] = data[key].primitive
        return cls(**data)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}