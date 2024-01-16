from pydantic import UUID4, BaseModel


class FindUserQuery(BaseModel):
    id: UUID4
    user_id: UUID4

    class Config:
        allow_mutation = False
