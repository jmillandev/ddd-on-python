from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserCommand:
    id: str
    email: str
    name: str
    last_name: str
    password: str
    pronoun: str
