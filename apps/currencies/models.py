from sqlalchemy import Column, String

from db.base_class import Base


class Currency(Base):
    code = Column(String(5), nullable=False, unique=True)
    description = Column(String(50), nullable=False)
