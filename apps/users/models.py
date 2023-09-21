from sqlalchemy import Boolean, Column, Enum, String

from apps.users.types import Pronoun
from db.base_class import Base


class User(Base):
    email = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    pronoun = Column(Enum(Pronoun, values_callable=lambda x: Pronoun.keys(), name='pronouns'))

    def __str__(self) -> str:
        return f"< {self.public_id} > {self.name} {self.last_name}"

    @property
    def password(self):
        return getattr(self, '_password')
    
    @password.setter
    def password(self, value):
        self._password = value
        # TODO TAS-21: Encrypt Password
        self.hashed_password = value
