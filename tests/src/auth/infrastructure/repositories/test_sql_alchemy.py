import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.infrastructure.repositories.sqlalchemy import SqlAlcheamyAuthCredentialRepository
from tests.src.auth.factories import AuthCredentialFactory
from src.users.infrastructure.repositories.sqlalchemy import SqlAlcheamyUserRepository
from tests.src.users.factories import UserFactory

pytestmark = pytest.mark.anyio


class TestSqlAlchemyAuthCredentialRepository:

    async def test_should_return_a_credentials(self, db_session: AsyncSession):
        # TODO: Create a Credential Table and propagate user changes to it. Actually, the credential table is a view
        attrs = UserFactory.to_dict()
        user_repository = SqlAlcheamyUserRepository(db_session)
        credential_repository = SqlAlcheamyAuthCredentialRepository(db_session)
        user = UserFactory.build(**attrs)
        credential = AuthCredentialFactory.build(
            user_id=attrs['id'],
            username=attrs['email'],
            password=attrs['password']
        )

        await user_repository.create(user)
        assert credential == await credential_repository.find(credential.username)

    async def test_should_not_return_a_non_existing_credential(self, db_session: AsyncSession):
        repository = SqlAlcheamyAuthCredentialRepository(db_session)
        credential = AuthCredentialFactory.build()

        assert await repository.find(credential.username) == None
