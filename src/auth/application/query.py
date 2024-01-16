from typing import Optional
from pydantic import BaseModel


class FindAuthTokenQuery(BaseModel):
    access_token: Optional[str]

    class Config:
        allow_mutation = False
