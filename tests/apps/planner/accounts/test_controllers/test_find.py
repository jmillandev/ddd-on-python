import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from kink import di
from sqlalchemy.ext.asyncio import AsyncSession

from apps.planner.backend.config import settings
from src.planner.accounts.domain.repository import AccountRepository
from src.planner.users.domain.repository import UserRepository
from tests.apps.planner.shared.auth import AuthAsUser
from tests.src.planner.shared.factories.accounts import AccountFactory
from tests.src.planner.users.factories import UserFactory

fake = Faker()

pytestmark = pytest.mark.anyio


class TestCreateAccountController:
    def setup_method(self):
        self._user = UserFactory.build()
        self._account = AccountFactory.build(owner_id=self._user.id.primitive)
        self._url = f"{settings.API_PREFIX}/v1/accounts/{self._account.id.primitive}"

    async def test_success(
        self, client: AsyncClient, sqlalchemy_sessionmaker: type[AsyncSession]
    ) -> None:
        await di[UserRepository].create(self._user)  # type: ignore[type-abstract]
        await di[AccountRepository].save(self._account)  # type: ignore[type-abstract]

        response = await client.get(self._url, auth=AuthAsUser(self._user.id))

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == {
            "id": self._account.id.primitive,
            "name": self._account.name.primitive,
            "currency": self._account.currency.primitive,
            "balance": self._account.balance.primitive,
            "owner_id": self._account.owner_id.primitive,
        }

    async def test_should_return_not_found(
        self, client: AsyncClient, sqlalchemy_sessionmaker: type[AsyncSession]
    ) -> None:
        response = await client.get(self._url, auth=AuthAsUser(self._user.id))

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text

        json_response = response.json()
        assert len(json_response["detail"]) == 1

        error_response = json_response["detail"][0]
        assert error_response["msg"] == "Account not found"
        assert error_response["source"] == "unknown"

    async def test_should_return_unauthorized_missing_token(
        self, client: AsyncClient, sqlalchemy_sessionmaker: type[AsyncSession]
    ) -> None:
        response = await client.get(self._url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text

        json_response = response.json()
        assert len(json_response["detail"]) == 1
        error_response = json_response["detail"][0]
        assert error_response["msg"] == "Is required"
        assert error_response["source"] == "access_token"
