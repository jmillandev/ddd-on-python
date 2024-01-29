from dataclasses import dataclass, field
from uuid import uuid4

from faker import Faker

from src.planner.auth_token.domain.entity import AuthCredential
from tests.src.shared.domain.factories import AggregateRootFactory

fake = Faker()


@dataclass
class AuthCredentialFactory(AggregateRootFactory[AuthCredential]):
    _AgregateClass = AuthCredential

    user_id: str = field(default_factory=lambda: str(uuid4()))
    username: str = field(default_factory=fake.email)
    password: str = field(default_factory=fake.password)
