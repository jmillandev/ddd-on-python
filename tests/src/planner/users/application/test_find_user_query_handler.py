from unittest.mock import Mock

import pytest

from src.planner.shared.domain.exceptions.base import DomainException
from src.planner.shared.domain.exceptions.forbidden import ForbiddenAccess
from src.planner.users.application.find.finder import UserFinder
from src.planner.users.application.find.query import FindUserQuery
from src.planner.users.application.find.query_handler import FindUserQueryHandler
from src.planner.users.application.find.responses import UserResponse
from src.planner.users.domain.exceptions.not_found import UserNotFound
from src.planner.users.domain.repository import UserRepository
from src.shared.domain.exceptions.not_found import NotFound
from tests.src.planner.users.factories import UserFactory

pytestmark = pytest.mark.anyio


class TestFindUserQueryHandler:
    def setup_method(self):
        self._repository = Mock(UserRepository)
        use_case = UserFinder(self._repository)
        self.handler = FindUserQueryHandler(use_case)

    async def test_should_return_a_user(self) -> None:
        user = UserFactory.build()
        self._repository.search.return_value = user
        query = FindUserQuery(id=user.id.primitive, user_id=user.id.primitive)

        response = await self.handler(query)
        assert isinstance(response, UserResponse)

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

        assert isinstance(excinfo.value, NotFound)
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
