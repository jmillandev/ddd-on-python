from pydantic import BaseModel, ConfigDict


class CreateAuthTokenCommand(BaseModel):
    model_config = ConfigDict(frozen=True)
    username: str
    password: str
