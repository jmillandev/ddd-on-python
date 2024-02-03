from dataclasses import dataclass


@dataclass(frozen=True)
class FindAccountQuery:
    id: str
    user_id: str
