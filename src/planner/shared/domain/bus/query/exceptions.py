from . import Query


class QueryNotRegistered(Exception):

    def __init__(self, query: Query) -> None:
        self.query = query
        super().__init__(f"Mising QueryHandler for <{query.__class__}>")
