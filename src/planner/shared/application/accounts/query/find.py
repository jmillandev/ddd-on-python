from dataclasses import dataclass


@dataclass(frozen=True)
class FindAccountQuery:
    id: str
    owner_id: str
