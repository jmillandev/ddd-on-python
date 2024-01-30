import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from kink import di
from sqlalchemy.ext.asyncio import AsyncSession

from apps.planner.backend.config import settings
from src.planner.users.domain.repository import UserRepository
from tests.apps.planner.shared.auth import AuthAsUser
from tests.src.planner.accounts.factories import AccountFactory
from tests.src.planner.users.factories import UserFactory

fake = Faker()

pytestmark = pytest.mark.anyio


class TestCreateAccountController:
    def setup_method(self):
        self._user = UserFactory.build()
        self._account = AccountFactory.build()
        self._url = f"{settings.API_PREFIX}/v1/accounts/{self._account.id.primitive}"
        self.params = {
            "name": self._account.name.primitive,
            "balance": self._account.balance.primitive,
            "currency": self._account.currency.primitive,
        }

    async def test_success(
        self, client: AsyncClient, sqlalchemy_session: AsyncSession
    ) -> None:
        await di[UserRepository].create(self._user)  # type: ignore[type-abstract]

        response = await client.post(
            self._url, auth=AuthAsUser(self._user.id), json=self.params
        )

        assert response.status_code == status.HTTP_201_CREATED, response.text
        assert response.json() is None

    async def test_should_return_unauthorized_missing_token(
        self, client: AsyncClient, sqlalchemy_session: AsyncSession
    ) -> None:
        response = await client.post(self._url, json=self.params)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text

        json_response = response.json()
        assert len(json_response["detail"]) == 1
        error_response = json_response["detail"][0]
        assert error_response["msg"] == "Is required"
        assert error_response["source"] == "access_token"
