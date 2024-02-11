from typing import Optional, Union

from src.planner.movements.domain.aggregate import Movement
from src.planner.movements.domain.expenses.aggregate import ExpenseMovement
from src.planner.movements.domain.incomes.aggregate import IncomeMovement
from src.planner.movements.domain.value_objects.id import MovementId
from src.planner.shared.application.mappers import dict_to_entity
from src.planner.shared.infrastructure.persistence.motor.repositories import (
    MotorRepository,
)


class MotorMovementRepository(MotorRepository):
    COLLECTION_NAME = "planner__movements"
    TYPES = {
        "ExpenseMovement": ExpenseMovement,
        "IncomeMovement": IncomeMovement,
    }

    async def save(self, movement: Movement) -> None:
        await self.collection.update_one(
            {"id": movement.id.value},
            {"$set": self.aggregate_to_dict(movement)},
            upsert=True,
        )

    async def search(self, id: MovementId) -> Optional[Union[ExpenseMovement, IncomeMovement]]:
        """Search object by id"""
        result = await self.collection.find_one({"id": id.value})
        if not result:
            return None

        return dict_to_entity(result, self.TYPES[result["_type"]])
