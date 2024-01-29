from dataclasses import dataclass, field
from uuid import uuid4

from faker import Faker

from src.planner.accounts.domain.entity import Account
from src.planner.accounts.domain.value_objects.currency import Currency
from tests.src.shared.domain.factories import AggregateRootFactory

fake = Faker()


@dataclass
class AccountFactory(AggregateRootFactory[Account]):
    _AgregateClass = Account

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=fake.word)
    currency: str = field(
        default_factory=lambda: fake.random_element(elements=Currency.keys())
    )
    user_id: str = field(default_factory=lambda: str(uuid4()))
    balance: int = field(default=0)
