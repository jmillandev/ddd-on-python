import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.planner.auth_token.domain.entity import AuthCredential
from src.planner.auth_token.domain.value_objects import AuthPassword, AuthUsername
from src.planner.auth_token.infrastructure.repositories.sqlalchemy import (
    SqlAlchemyAuthCredentialRepository,
)
from src.planner.shared.domain.users import UserId
from src.planner.users.infrastructure.repositories.sqlalchemy import (
    SqlAlchemyUserRepository,
)
from tests.src.planner.auth_token.factories import AuthCredentialFactory
from tests.src.planner.users.factories import UserFactory

pytestmark = pytest.mark.anyio


class TestSqlAlchemyAuthCredentialRepository:
    async def test_should_return_a_credentials(
        self, sqlalchemy_sessionmaker: type[AsyncSession]
    ):
        # TODO: Create a Credential Table and propagate user changes to it. Actually, the credential table is a view  # noqa:E501
        attrs = UserFactory.to_dict()
        user_repository = SqlAlchemyUserRepository(sqlalchemy_sessionmaker)
        credential_repository = SqlAlchemyAuthCredentialRepository(
            sqlalchemy_sessionmaker
        )
        user = UserFactory.build(**attrs)
        credential = AuthCredential(
            user_id=UserId(attrs["id"]),
            username=AuthUsername(attrs["email"]),
            password=AuthPassword(user.password.value, is_hashed=True),  # type: ignore[call-arg]
        )

        await user_repository.create(user)
        assert credential == await credential_repository.search(credential.username)

    async def test_should_not_return_a_non_existing_credential(
        self, sqlalchemy_sessionmaker: type[AsyncSession]
    ):
        repository = SqlAlchemyAuthCredentialRepository(sqlalchemy_sessionmaker)
        credential = AuthCredentialFactory.build()

        assert await repository.search(credential.username) is None
