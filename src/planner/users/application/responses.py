from src.planner.users.domain.value_objects.pronoun import Pronoun
from dataclasses import dataclass


@dataclass(frozen=True)
class UserResponse:
    id: str
    email: str
    name: str
    last_name: str
    pronoun: Pronoun
