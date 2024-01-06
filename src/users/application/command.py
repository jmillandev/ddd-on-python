from pydantic import BaseModel, EmailStr, UUID4
from src.users.domain.value_objects.pronoun import Pronoun


class CreateUserCommand(BaseModel):
    id: UUID4
    email: EmailStr
    name: str
    last_name: str
    password: str
    pronoun: Pronoun

    class Config:
        allow_mutation = False
