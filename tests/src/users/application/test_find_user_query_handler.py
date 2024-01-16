from unittest.mock import Mock

import pytest

from src.shared.application.response import Response
from src.shared.domain.exceptions.base import DomainException
from src.users.application.finder import UserFinder
from src.users.application.query import FindUserQuery
from src.users.application.query_handler import FindUserQueryHandler
from src.users.application.responses import UserResponse
from src.users.domain.exceptions.not_found import UserNotFound
from src.users.domain.repository import UserRepository
from tests.src.users.factories import UserFactory

pytestmark = pytest.mark.anyio

class TestFindUserQueryHandler:
    def setup(self):
        self._repository = Mock(UserRepository)
        use_case = UserFinder(self._repository)
        self.handler = FindUserQueryHandler(use_case)

    async def test_should_return_a_user(self) -> None:
        params = UserFactory.to_dict()
        user = UserFactory.build(**params)
        self._repository.search.return_value = user
        query = FindUserQuery(id=params['id'], user_id=user.id.primitive)

        response = await self.handler(query)
        assert isinstance(response, UserResponse)
        assert isinstance(response, Response)

        self._repository.search.assert_called_once_with(user.id)

    async def test_should_raise_error_user_not_found(self) -> None:
        params = UserFactory.to_dict()
        self._repository.search.return_value = None
        query = FindUserQuery(id=params['id'], user_id=params['id'])

        with pytest.raises(UserNotFound) as excinfo:
            await self.handler(query)

        assert isinstance(excinfo.value, DomainException)
        assert excinfo.value.code == 404

    @pytest.mark.skip(reason="TODO: Not implemented")
    async def test_should_raise_forbidden_error(self) -> None:
        # user = await UserFactory()

        # response = await client.post(f"{settings.API_PREFIX}/v1/users/{user.public_id}", auth=AuthAsUser(await UserFactory()))

        # assert response.status_code == status.HTTP_403_FORBIDDEN, response.text

        # json_response = response.json()
        # assert len(json_response['detail']) == 1
        # error_response = json_response['detail'][0]
        # assert error_response['msg'] == 'You do not have permission to perform this action'
        # assert error_response['source'] == 'credentials'
        ...