from src.auth.application.query import FindAuthTokenQuery
from src.auth.application.query_handler import FindAuthTokenQueryHandler
from src.shared.domain.bus.query import Query, QueryResponse
from src.shared.domain.bus.query.exceptions import QueryNotRegistered
from src.users.application.query import FindUserQuery
from src.users.application.query_handler import FindUserQueryHandler


class HardcodedQueryBus:

    HANDLERS = {
        FindUserQuery: FindUserQueryHandler,
        FindAuthTokenQuery: FindAuthTokenQueryHandler
    }

    async def ask(self, command: Query)-> QueryResponse:
        try:
            return await self.HANDLERS[command.__class__]()(command)
        except KeyError:
            raise QueryNotRegistered(command)
