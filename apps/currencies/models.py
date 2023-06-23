from sqlalchemy import Column, String

from db.base_class import Base


class Currency(Base):
    __tablename__ = "currencies"

    code = Column(String(5), nullable=False, unique=True, index=True)
    description = Column(String(50), nullable=False)
