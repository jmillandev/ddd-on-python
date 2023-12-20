from datetime import datetime
from src.users.domain.entity import User
from src.users.domain.value_objects import *
from src.users.domain.value_objects.pronoun import Pronoun

from faker import Faker

from uuid import uuid4

fake = Faker()


class UserFactory:
    
    @staticmethod
    def build( 
            id: str = uuid4(),
            created_at: datetime = datetime.utcnow(),
            email: str = fake.email(),
            name: str = fake.first_name(),
            last_name: str = fake.last_name(),
            is_active: bool = True,
            pronoun: str = fake.random_element(elements=Pronoun.keys()),
            password: str = fake.password()
        ) -> User:
        return User(
            id=UserId(id),
            created_at=UserCreatedAt(created_at),
            email=UserEmail(email),
            name=UserName(name),
            last_name=UserLastName(last_name),
            is_active=UserIsActive(is_active),
            pronoun=UserPronoun(pronoun),
            password=UserPassword(password)
        )
1