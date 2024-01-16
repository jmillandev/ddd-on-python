from pydantic import BaseModel, UUID4


class CreateUserCommand(BaseModel):
    id: UUID4
    email: str
    name: str
    last_name: str
    password: str
    pronoun: str

    class Config:
        allow_mutation = False
