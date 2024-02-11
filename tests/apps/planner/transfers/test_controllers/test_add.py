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
from tests.src.planner.movements.factories import TransferMovementFactory
from tests.src.planner.shared.factories.accounts import AccountFactory
from tests.src.planner.users.factories import UserFactory

fake = Faker()

pytestmark = pytest.mark.anyio


class TestAddTransferMovementController:
    def setup_method(self):
        self._user = UserFactory.build()
        self._origin = AccountFactory.build(owner_id=self._user.id.primitive)
        self._destination = AccountFactory.build(owner_id=self._user.id.primitive)
        self._transfer = TransferMovementFactory.build(
            origin_id=self._origin.id.primitive,
            destination_id=self._destination.id.primitive,
        )
        self._url = f"{settings.API_PREFIX}/v1/transfers/{self._transfer.id.primitive}"
        self.params = {
            "amount": self._transfer.amount.primitive,
            "origin_id": self._transfer.origin_id.primitive,
            "destination_id": self._transfer.destination_id.primitive,
            "date": self._transfer.date.primitive,
        }

    async def test_success(
        self,
        client: AsyncClient,
        sqlalchemy_session: AsyncSession,
        motor_database: AgnosticDatabase,
    ) -> None:
        await di[UserRepository].create(self._user)  # type: ignore[type-abstract]
        await di[AccountRepository].save(self._origin)  # type: ignore[type-abstract]
        await di[AccountRepository].save(self._destination)  # type: ignore[type-abstract]
        # TODO: Use Factory to create Account

        response = await client.post(
            self._url, auth=AuthAsUser(self._user.id), json=self.params
        )

        assert response.status_code == status.HTTP_201_CREATED, response.text
        assert response.json() is None

    async def test_should_return_unauthorized_missing_token(
        self,
        client: AsyncClient,
        sqlalchemy_session: AsyncSession,
        motor_database: AgnosticDatabase,
    ) -> None:
        response = await client.post(self._url, json=self.params)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text

        json_response = response.json()
        assert len(json_response["detail"]) == 1
        error_response = json_response["detail"][0]
        assert error_response["msg"] == "Is required"
        assert error_response["source"] == "access_token"
