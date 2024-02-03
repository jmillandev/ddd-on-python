from unittest.mock import Mock

import pytest

from src.planner.accounts.application.find.query_handler import (
    FindAccountQueryHandler,
)
from src.planner.accounts.application.find.finder import AccountFinder
from src.planner.shared.application.accounts.query import FindAccountQuery
from src.planner.shared.application.accounts.response import AccountResponse
from src.planner.accounts.domain.repository import AccountRepository
from src.shared.domain.exceptions.not_found import NotFound
from tests.src.planner.shared.factories.accounts import AccountFactory
from src.planner.accounts.domain.exceptions.not_found import AccountNotFound

pytestmark = pytest.mark.anyio


class TestFindAccountQueryHandler:
    def setup_method(self):
        self._repository = Mock(AccountRepository)
        use_case = AccountFinder(self._repository)
        self.handler = FindAccountQueryHandler(use_case)

    async def test_should_return_an_account(self) -> None:
        account = AccountFactory.build()
        self._repository.search_by_id_and_user_id.return_value = account
        query = FindAccountQuery(id=account.id.primitive, user_id=account.user_id.primitive)

        response = await self.handler(query)
        assert isinstance(response, AccountResponse)

        self._repository.search_by_id_and_user_id.assert_called_once_with(account.id, account.user_id)

    async def test_should_raise_error_account_not_found(self) -> None:
        params = AccountFactory().to_dict()
        self._repository.search_by_id_and_user_id.return_value = None
        query = FindAccountQuery(id=params['id'], user_id=params['user_id'])

        with pytest.raises(AccountNotFound) as excinfo:
            await self.handler(query)

        assert isinstance(excinfo.value, NotFound)
        assert excinfo.value.code == 404
