from datetime import datetime
from src.users.domain.entity import User
from src.users.domain.value_objects import *
from src.users.domain.value_objects.pronoun import Pronoun

from faker import Faker

from uuid import uuid4

fake = Faker()


class UserFactory:
    
    @staticmethod
    def build(**kwargs) -> User:
        attrs = UserFactory.to_dict(**kwargs)
        return User.from_dict(attrs)

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