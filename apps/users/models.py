from sqlalchemy import Boolean, Column, Enum, String

from apps.users.types import Pronoun
from db.base_class import Base
from utils.passwords import password_context


class User(Base):
    email = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    pronoun = Column(
        Enum(Pronoun, values_callable=lambda x: Pronoun.keys(), name='pronouns'))

    def __str__(self) -> str:
        return f"< {self.public_id} > {self.name} {self.last_name}"

    @property
    def password(self):
        return None

    @password.setter
    def password(self, value):
        self._password = value
        self.hashed_password = password_context.hash(value)

    def verify_password(self, password):
        return password_context.verify(password, self.hashed_password)
