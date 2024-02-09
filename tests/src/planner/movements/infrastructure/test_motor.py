import pytest
from motor.core import AgnosticDatabase

from src.planner.movements.domain.repository import MovementRepository
from src.planner.movements.infrastructure.repositories.motor import (
    MotorMovementRepository,
)
from tests.src.planner.movements.factories import ExpenseMovementFactory

pytestmark = pytest.mark.anyio


class TestMotorMovementRepositoryWithExpenses:
    def setup_method(self):
        self.expense = ExpenseMovementFactory.build()

    def test_should_be_a_valid_repository(self):
        assert issubclass(MotorMovementRepository, MovementRepository)

    async def test_should_create_a_movement(self, motor_database: AgnosticDatabase):
        repository = MotorMovementRepository(motor_database)

        await repository.save(self.expense)

    async def test_should_not_return_a_non_existing_expense(
        self, motor_database: AgnosticDatabase
    ):
        repository = MotorMovementRepository(motor_database)

        assert await repository.search(self.expense.id) is None

    async def test_should_return_an_expense_by_id(
        self, motor_database: AgnosticDatabase
    ):
        repository = MotorMovementRepository(motor_database)

        await repository.save(self.expense)
        perssisted_expense = await repository.search(self.expense.id)
        assert self.expense == perssisted_expense
