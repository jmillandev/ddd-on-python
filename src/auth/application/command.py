from pydantic import BaseModel


class CreateAuthTokenCommand(BaseModel):
    username: str
    password: str

    class Config:
        allow_mutation = False
