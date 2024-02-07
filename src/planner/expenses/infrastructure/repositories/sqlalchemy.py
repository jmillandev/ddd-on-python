from kink import inject
from sqlalchemy import UUID, Column, Date, Integer

from src.planner.expenses.domain.entity import Expense
from src.planner.shared.infrastructure.persistence.sqlalchemy.models import Base
from src.planner.shared.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyFindMixin,
    SqlAlchemyRepository,
    SqlAlchemySaveMixin,
)


class SqlAlchemyExpense(Base):
    id = Column(UUID, primary_key=True)
    amount = Column(Integer)
    account_id = Column(UUID)
    date = Column(Date)
    __tablename__ = "movements__accounts"


@inject
class SqlAlchemyExpenseRepository(
    SqlAlchemyRepository, SqlAlchemyFindMixin, SqlAlchemySaveMixin
):
    model_class = SqlAlchemyExpense
    entity_class = Expense
