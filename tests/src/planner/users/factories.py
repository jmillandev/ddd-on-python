from datetime import datetime
from typing import Optional
from uuid import uuid4

from faker import Faker

from src.planner.shared.application.mappers import dict_to_entity
from src.planner.users.domain.entity import User
from src.planner.users.domain.value_objects.pronoun import Pronoun

fake = Faker()


class UserFactory:
    @classmethod
    def build(cls, **kwargs) -> User:
        return dict_to_entity(cls.to_dict(**kwargs), User)

    @staticmethod
    def to_dict(
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        last_name: Optional[str] = None,
        pronoun: Optional[str] = None,
        password: Optional[str] = None,
        is_active: Optional[bool] = True,
    ) -> dict:
        return {
            "id": id or uuid4(),
            "created_at": created_at or datetime.utcnow(),
            "email": email or fake.email(),
            "name": name or fake.first_name(),
            "last_name": last_name or fake.last_name(),
            "is_active": is_active,
            "pronoun": pronoun or fake.random_element(elements=Pronoun.keys()),
            "password": password or fake.password(),
        }
