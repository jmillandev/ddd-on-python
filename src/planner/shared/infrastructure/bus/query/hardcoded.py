from src.planner.auth_token.application.find.query import FindAuthTokenQuery
from src.planner.auth_token.application.find.query_handler import (
    FindAuthTokenQueryHandler,
)
from src.planner.shared.domain.bus.query import Query, QueryResponse
from src.planner.shared.domain.bus.query.exceptions import QueryNotRegistered
from src.planner.users.application.find.query import FindUserQuery
from src.planner.users.application.find.query_handler import FindUserQueryHandler
from src.planner.shared.application.accounts.query import FindAccountQuery
from src.planner.accounts.application.find.query_handler import FindAccountQueryHandler

class HardcodedQueryBus:
    HANDLERS = {
        FindUserQuery: FindUserQueryHandler,
        FindAuthTokenQuery: FindAuthTokenQueryHandler,
        FindAccountQuery: FindAccountQueryHandler,
    }

    async def ask(self, command: Query) -> QueryResponse:
        try:
            return await self.HANDLERS[command.__class__]()(command)
        except KeyError:
            raise QueryNotRegistered(command)
