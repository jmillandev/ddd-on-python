from datetime import datetime
from src.users.domain.entity import User
from src.users.domain.value_objects import *
from faker import Faker

from uuid import uuid4

fake = Faker()

class UserFactory:
    
    @staticmethod
    def build(
            self, 
            id: str = uuid4(),
            created_at: datetime = datetime.utcnow(),
            email: str = fake.email(),
            name: str = fake.first_name(),
            last_name: str = fake.last_name(),
            is_active: bool = True,
            pronoun: str = None,
            password: str = fake.password()
        ) -> User:
        User(
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