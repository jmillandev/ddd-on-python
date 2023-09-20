from sqlalchemy import Boolean, Column, String, Enum

from db.base_class import Base
import enum


class Pronoun(str, enum.Enum):
    HE = 'he'
    SHE = 'she'

    @staticmethod
    def keys():
        return [c.value for c in Pronoun]

class User(Base):
    email = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    pronoun = Column(Enum(Pronoun, values_callable=lambda x: Pronoun.keys(), name='pronouns'))

    def __str__(self) -> str:
        return f"< {self.public_id} > {self.name} {self.last_name}"
