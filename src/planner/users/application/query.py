from dataclasses import dataclass

@dataclass(frozen=True)
class FindUserQuery:
    id: str
    user_id: str
