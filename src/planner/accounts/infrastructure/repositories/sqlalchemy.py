from typing import Optional

from kink import inject
from sqlalchemy import UUID, Column, Integer, String, select

from src.planner.accounts.domain.entity import Account
from src.planner.accounts.domain.value_objects import AccountName
from src.planner.shared.domain.users import UserId
from src.planner.shared.infrastructure.persistence.sqlalchemy.models import Base
from src.planner.shared.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlcheamyCreateMixin,
    SqlAlcheamyRepository,
    SqlAlcheamySearchMethodMixin,
)


class SqlAlcheamyAccount(Base):
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID)
    name = Column(String)
    currency = Column(String)
    balance = Column(Integer)
    __tablename__ = "accounts"


@inject
class SqlAlcheamyAccountRepository(
    SqlAlcheamyRepository, SqlAlcheamySearchMethodMixin, SqlAlcheamyCreateMixin
):
    model_class = SqlAlcheamyAccount
    entity_class = Account

    async def search_by_name_and_user_id(
        self, name: AccountName, user_id: UserId
    ) -> Optional[Account]:
        stmt = (
            select(SqlAlcheamyAccount)
            .filter_by(name=name.value, user_id=user_id.value)
            .limit(1)
        )
        return await self._search(stmt)
