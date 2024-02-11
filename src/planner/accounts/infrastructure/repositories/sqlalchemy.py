from typing import Optional

from kink import inject
from sqlalchemy import UUID, Column, Integer, String, select

from src.planner.accounts.domain.entity import Account
from src.planner.accounts.domain.repository import AccountRepository
from src.planner.accounts.domain.value_objects import AccountName
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.users import UserId
from src.planner.shared.infrastructure.persistence.sqlalchemy.models import Base
from src.planner.shared.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyFindMixin,
    SqlAlchemyRepository,
    SqlAlchemySaveMixin,
)


class SqlAlchemyAccount(Base):
    id = Column(UUID, primary_key=True)
    owner_id = Column(UUID)
    name = Column(String)
    currency = Column(String)
    balance = Column(Integer)
    __tablename__ = "planner__accounts"


@inject(alias=AccountRepository, use_factory=True)
class SqlAlchemyAccountRepository(
    SqlAlchemyRepository, SqlAlchemyFindMixin, SqlAlchemySaveMixin
):
    model_class = SqlAlchemyAccount
    entity_class = Account

    async def search_by_name_and_owner_id(
        self, name: AccountName, owner_id: UserId
    ) -> Optional[Account]:
        stmt = (
            select(SqlAlchemyAccount)
            .filter_by(name=name.value, owner_id=owner_id.value)
            .limit(1)
        )
        return await self._search(stmt)

    async def search_by_id_and_owner_id(
        self, id: AccountId, owner_id: UserId
    ) -> Optional[Account]:
        stmt = (
            select(SqlAlchemyAccount)
            .filter_by(id=id.value, owner_id=owner_id.value)
            .limit(1)
        )
        return await self._search(stmt)
