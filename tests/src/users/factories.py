from datetime import datetime
from uuid import uuid4

from faker import Faker

from src.shared.application.mappers import dict_to_entity
from src.users.domain.entity import User
from src.users.domain.value_objects import *
from src.users.domain.value_objects.pronoun import Pronoun

fake = Faker()


class UserFactory:
    
    @classmethod
    def build(cls, **kwargs) -> User:
        return dict_to_entity(cls.to_dict(**kwargs), User)

    @staticmethod
    def to_dict( 
            id: str = uuid4(),
            created_at: datetime = datetime.utcnow(),
            email: str = fake.email(),
            name: str = fake.first_name(),
            last_name: str = fake.last_name(),
            is_active: bool = True,
            pronoun: str = fake.random_element(elements=Pronoun.keys()),
            password: str = fake.password()
        ) -> dict:
        return {
            'id': id,
            'created_at': created_at,
            'email': email,
            'name': name,
            'last_name': last_name,
            'is_active': is_active,
            'pronoun': pronoun,
            'password': password
        }
