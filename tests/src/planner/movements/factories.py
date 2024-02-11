from dataclasses import dataclass, field
from uuid import uuid4

from faker import Faker

from src.planner.movements.domain.expenses.aggregate import ExpenseMovement
from src.planner.movements.domain.incomes.aggregate import IncomeMovement
from src.planner.shared.domain.movements.events import (
    ExpenseMovementAdded,
    IncomeMovementAdded,
)
from src.planner.shared.domain.value_objects.date import DATE_FORMAT
from tests.src.shared.domain.factories import AggregateRootFactory, EventDomainFactory

fake = Faker()


@dataclass
class ExpenseMovementFactory(AggregateRootFactory[ExpenseMovement]):
    _AgregateClass = ExpenseMovement

    id: str = field(default_factory=lambda: str(uuid4()))
    amount: int = field(default_factory=fake.pyint)
    account_id: str = field(default_factory=lambda: str(uuid4()))
    date: str = field(default_factory=lambda: fake.date_object().strftime(DATE_FORMAT))


@dataclass
class ExpenseMovementAddedFactory(EventDomainFactory[ExpenseMovementAdded]):
    _EventClass = ExpenseMovementAdded

    amount: int = field(default_factory=fake.pyint)
    account_id: str = field(default_factory=lambda: str(uuid4()))
    date: str = field(default_factory=lambda: fake.date_object().strftime(DATE_FORMAT))


@dataclass
class IncomeMovementFactory(AggregateRootFactory[IncomeMovement]):
    _AgregateClass = IncomeMovement

    id: str = field(default_factory=lambda: str(uuid4()))
    amount: int = field(default_factory=fake.pyint)
    account_id: str = field(default_factory=lambda: str(uuid4()))
    date: str = field(default_factory=lambda: fake.date_object().strftime(DATE_FORMAT))


@dataclass
class IncomeMovementAddedFactory(EventDomainFactory[IncomeMovementAdded]):
    _EventClass = IncomeMovementAdded

    amount: int = field(default_factory=fake.pyint)
    account_id: str = field(default_factory=lambda: str(uuid4()))
    date: str = field(default_factory=lambda: fake.date_object().strftime(DATE_FORMAT))
