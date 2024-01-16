from pydantic import BaseModel, UUID4


class FindUserQuery(BaseModel):
    id: UUID4

    class Config:
        allow_mutation = False
