from src.planner.auth_token.application.find.query import FindAuthTokenQuery
from src.planner.auth_token.application.find.query_handler import (
    FindAuthTokenQueryHandler,
)
from src.planner.shared.domain.bus.query import Query, QueryResponse
from src.planner.shared.domain.bus.query.exceptions import QueryNotRegistered
from src.planner.users.application.find.query import FindUserQuery
from src.planner.users.application.find.query_handler import FindUserQueryHandler


class HardcodedQueryBus:
    HANDLERS = {
        FindUserQuery: FindUserQueryHandler,
        FindAuthTokenQuery: FindAuthTokenQueryHandler,
    }

    async def ask(self, command: Query) -> QueryResponse:
        try:
            return await self.HANDLERS[command.__class__]()(command)
        except KeyError:
            raise QueryNotRegistered(command)
