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


class TestUpdateUserAvatarController:
    def setup_method(self):
        self._user = UserFactory.build()
        self._url = f"{settings.API_PREFIX}/v1/users/{self._user.id}/avatar"

    async def test_success(
        self, client: AsyncClient, sqlalchemy_sessionmaker: type[AsyncSession]
    ) -> None:
        await di[UserRepository].create(self._user)  # type: ignore[type-abstract]

        response = await client.put(
            self._url,
            auth=AuthAsUser(self._user.id),
            files={"avatar": ("sample.jpg", open('tests/fixtures/files/sample.jpg', "rb"), "image/jpeg")}
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == None

    async def test_should_return_unauthorized_missing_token(
        self, client: AsyncClient, sqlalchemy_sessionmaker: type[AsyncSession]
    ) -> None:
        response = await client.put(self._url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text

        json_response = response.json()
        assert len(json_response["detail"]) == 1
        error_response = json_response["detail"][0]
        assert error_response["msg"] == "Is required"
        assert error_response["source"] == "access_token"
