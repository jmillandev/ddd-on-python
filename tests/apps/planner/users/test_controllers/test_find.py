import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from kink import di
from sqlalchemy.ext.asyncio import AsyncSession

from apps.planner.backend.config import settings
from src.planner.users.domain.repository import UserRepository
from tests.apps.planner.shared.auth import AuthAsUser
from tests.src.planner.users.factories import UserFactory

fake = Faker()

pytestmark = pytest.mark.anyio


class TestFindController:
    def setup(self):
        self._user = UserFactory.build()

    async def test_success(
        self, client: AsyncClient, sqlalchemy_session: AsyncSession
    ) -> None:
        await di[UserRepository].create(self._user)  # type: ignore[type-abstract]

        response = await client.get(
            f"{settings.API_PREFIX}/v1/users/{self._user.id.primitive}",
            auth=AuthAsUser(self._user.id),
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == {
            "id": self._user.id.primitive,
            "name": self._user.name.primitive,
            "email": self._user.email.primitive,
            "last_name": self._user.last_name.primitive,
            "pronoun": self._user.pronoun.primitive,
        }

    async def test_should_return_unauthorized_missing_token(
        self, client: AsyncClient, sqlalchemy_session: AsyncSession
    ) -> None:
        response = await client.get(f"{settings.API_PREFIX}/v1/users/{self._user.id}")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text

        json_response = response.json()
        assert len(json_response["detail"]) == 1
        error_response = json_response["detail"][0]
        assert error_response["msg"] == "Is required"
        assert error_response["source"] == "access_token"

    @pytest.mark.skip(reason="TODO: Use Mock to return a invalid token")
    async def test_should_return_unauthorized_invalid_token(
        self, client: AsyncClient, sqlalchemy_session: AsyncSession
    ) -> None:
        user = UserFactory.build()

        response = await client.get(
            f"{settings.API_PREFIX}/v1/users/{user.id}", auth=AuthAsUser(self._user.id)
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text

        json_response = response.json()
        assert len(json_response["detail"]) == 1
        error_response = json_response["detail"][0]
        assert error_response["msg"] == "Is required"
        assert error_response["source"] == "access_token"
