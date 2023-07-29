from sqlalchemy import UUID, Column, Integer, DateTime, func

from sqlalchemy.orm import as_declarative, declared_attr
from uuid import uuid4

@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(UUID, unique=True, index=True, default=uuid4, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False
    )

    __name__: str
    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
