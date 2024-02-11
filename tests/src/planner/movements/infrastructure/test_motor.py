import pytest
from motor.core import AgnosticDatabase

from src.planner.movements.domain.repository import MovementRepository
from src.planner.movements.infrastructure.repositories.motor import (
    MotorMovementRepository,
)
from tests.src.planner.movements.factories import (
    ExpenseMovementFactory,
    IncomeMovementFactory,
    TransferMovementFactory,
)

pytestmark = pytest.mark.anyio


class TestMotorMovementRepository:
    def test_should_be_a_valid_repository(self):
        assert issubclass(MotorMovementRepository, MovementRepository)

    async def test_should_not_return_a_non_existing_movement(
        self, motor_database: AgnosticDatabase
    ):
        movement = ExpenseMovementFactory.build()
        repository = MotorMovementRepository(motor_database)

        assert await repository.search(movement.id) is None


class TestMotorMovementRepositoryWithExpenses:
    def setup_method(self):
        self.expense = ExpenseMovementFactory.build()

    async def test_should_create_a_expense(self, motor_database: AgnosticDatabase):
        repository = MotorMovementRepository(motor_database)

        await repository.save(self.expense)

    async def test_should_return_an_expense_by_id(
        self, motor_database: AgnosticDatabase
    ):
        repository = MotorMovementRepository(motor_database)

        await repository.save(self.expense)
        perssisted_expense = await repository.search(self.expense.id)
        assert self.expense == perssisted_expense


class TestMotorMovementRepositoryWithIncomes:
    def setup_method(self):
        self.income = IncomeMovementFactory.build()

    async def test_should_create_a_income(self, motor_database: AgnosticDatabase):
        repository = MotorMovementRepository(motor_database)

        await repository.save(self.income)

    async def test_should_return_an_income_by_id(
        self, motor_database: AgnosticDatabase
    ):
        repository = MotorMovementRepository(motor_database)

        await repository.save(self.income)
        perssisted_income = await repository.search(self.income.id)
        assert self.income == perssisted_income


class TestMotorMovementRepositoryWithTransfers:
    def setup_method(self):
        self.transfer = TransferMovementFactory.build()

    async def test_should_create_a_transfer(self, motor_database: AgnosticDatabase):
        repository = MotorMovementRepository(motor_database)

        await repository.save(self.transfer)

    async def test_should_return_an_transfer_by_id(
        self, motor_database: AgnosticDatabase
    ):
        repository = MotorMovementRepository(motor_database)

        await repository.save(self.transfer)
        perssisted_transfer = await repository.search(self.transfer.id)
        assert self.transfer == perssisted_transfer
