import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from kink import di
from motor.core import AgnosticDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from apps.planner.backend.config import settings
from src.planner.accounts.domain.repository import AccountRepository
from src.planner.users.domain.repository import UserRepository
from tests.apps.planner.shared.auth import AuthAsUser
from tests.src.planner.movements.factories import IncomeMovementFactory
from tests.src.planner.shared.factories.accounts import AccountFactory
from tests.src.planner.users.factories import UserFactory

fake = Faker()

pytestmark = pytest.mark.anyio


class TestAddIncomeMovementController:
    def setup_method(self):
        self._user = UserFactory.build()
        self._account = AccountFactory.build(owner_id=self._user.id.primitive)
        self._income = IncomeMovementFactory.build(
            account_id=self._account.id.primitive
        )
        self._url = f"{settings.API_PREFIX}/v1/incomes/{self._income.id.primitive}"
        self.params = {
            "amount": self._income.amount.primitive,
            "account_id": self._income.account_id.primitive,
            "date": self._income.date.primitive,
        }

    async def test_success(
        self,
        client: AsyncClient,
        sqlalchemy_sessionmaker: type[AsyncSession],
        motor_database: AgnosticDatabase,
    ) -> None:
        await di[UserRepository].create(self._user)  # type: ignore[type-abstract]
        await di[AccountRepository].save(self._account)  # type: ignore[type-abstract]
        # TODO: Use Factory to create Account

        response = await client.post(
            self._url, auth=AuthAsUser(self._user.id), json=self.params
        )

        assert response.status_code == status.HTTP_201_CREATED, response.text
        assert response.json() is None

    async def test_should_return_unauthorized_missing_token(
        self,
        client: AsyncClient,
        sqlalchemy_sessionmaker: type[AsyncSession],
        motor_database: AgnosticDatabase,
    ) -> None:
        response = await client.post(self._url, json=self.params)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text

        json_response = response.json()
        assert len(json_response["detail"]) == 1
        error_response = json_response["detail"][0]
        assert error_response["msg"] == "Is required"
        assert error_response["source"] == "access_token"
