from sqlalchemy import UUID, Column, Integer, DateTime

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(UUID, unique=True, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

