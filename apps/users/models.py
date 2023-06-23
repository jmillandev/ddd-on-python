from sqlalchemy import Boolean, Column, String

from db.base_class import Base


class User(Base):
    email = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    def __str__(self) -> str:
        return f"< {self.public_id} > {self.name} {self.last_name}"
