from src.shared.domain.bus.query import QueryResponse, Query
from src.shared.domain.bus.query.exceptions import QueryNotRegistered
from src.users.application.query_handler import FindUserQueryHandler
from src.users.application.query import FindUserQuery

class HardcodedQueryBus:

    HANDLERS = {
        FindUserQuery: FindUserQueryHandler
    }

    async def ask(self, command: Query)-> QueryResponse:
        try:
            return await self.HANDLERS[command.__class__]()(command)
        except KeyError:
            raise QueryNotRegistered(command)
