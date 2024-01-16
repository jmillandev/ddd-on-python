from pydantic import UUID4, BaseModel


class CreateUserCommand(BaseModel):
    id: UUID4
    email: str
    name: str
    last_name: str
    password: str
    pronoun: str

    class Config:
        allow_mutation = False
