from unittest.mock import Mock

import pytest

from src.planner.shared.application.response import Response
from src.planner.shared.domain.exceptions.base import DomainException
from src.planner.shared.domain.exceptions.forbidden import ForbiddenAccess
from src.planner.users.application.finder import UserFinder
from src.planner.users.application.query import FindUserQuery
from src.planner.users.application.query_handler import FindUserQueryHandler
from src.planner.users.application.responses import UserResponse
from src.planner.users.domain.exceptions.not_found import UserNotFound
from src.planner.users.domain.repository import UserRepository
from tests.src.planner.users.factories import UserFactory

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
        query = FindUserQuery(id=params["id"], user_id=user.id.primitive)

        response = await self.handler(query)
        assert isinstance(response, UserResponse)
        assert isinstance(response, Response)

        self._repository.search.assert_called_once_with(user.id)

    async def test_should_raise_error_user_not_found(self) -> None:
        """
        Test that the handler raises a UserNotFound exception when
        the user is not persisted yet.
        """
        params = UserFactory.to_dict()
        self._repository.search.return_value = None
        query = FindUserQuery(id=params["id"], user_id=params["id"])

        with pytest.raises(UserNotFound) as excinfo:
            await self.handler(query)

        assert isinstance(excinfo.value, DomainException)
        assert excinfo.value.code == 404

    async def test_should_raise_forbidden_error(self) -> None:
        params = UserFactory.to_dict()
        other_user = UserFactory.build()
        self._repository.search.return_value = None
        query = FindUserQuery(id=params["id"], user_id=other_user.id.primitive)

        with pytest.raises(ForbiddenAccess) as excinfo:
            await self.handler(query)

        assert isinstance(excinfo.value, DomainException)
        assert excinfo.value.code == 403
        assert excinfo.value.source == "credentials"
        assert excinfo.value.message == "You are not allowed to do this operation"
