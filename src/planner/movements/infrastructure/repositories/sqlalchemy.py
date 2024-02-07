from typing import Optional

from kink import inject
from sqlalchemy import UUID, Column, Date, Integer, Select, select

from src.planner.movements.domain.aggregate import Movement
from src.planner.movements.domain.expenses.aggregate import ExpenseMovement
from src.planner.movements.domain.value_objects.id import ExpenseId
from src.planner.shared.application.mappers import dict_to_entity
from src.planner.shared.infrastructure.persistence.sqlalchemy.models import Base
from src.planner.shared.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyRepository,
)


class SqlAlchemyExpense(Base):
    id = Column(UUID, primary_key=True)
    amount = Column(Integer)
    account_id = Column(UUID)
    date = Column(Date)
    __tablename__ = "movements__accounts"


@inject
class SqlAlchemyMovementRepository(SqlAlchemyRepository):
    model_class = SqlAlchemyExpense

    async def save(self, entity: Movement) -> None:
        entity_object = self.model_class.from_entity(entity)
        self.session.add(entity_object)
        await self.session.commit()
        return None

    async def search(self, id: ExpenseId) -> Optional[ExpenseMovement]:
        """Search object by id"""
        stmt = select(self.model_class).where(self.model_class.id == id.value).limit(1)  # type: ignore[attr-defined] # noqa: E501
        return await self._search(stmt)

    async def _search(self, stmt: Select) -> Optional[ExpenseMovement]:
        """Search movement by select statement"""
        result = await self.session.execute(stmt)
        data = result.scalars().first()
        if data:
            return dict_to_entity(data.to_dict(), ExpenseMovement)
        return None
