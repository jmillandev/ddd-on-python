from typing import Optional

from pydantic import BaseModel, EmailStr
from apps.users.types import Pronoun

class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    is_active: Optional[bool] = True
    name: str
    last_name: str
    pronoun: Optional[Pronoun]
    full_name: str

    @classmethod
    def from_orm(cls, user):
        return cls(
            id=str(user.public_id),
            email=user.email,
            is_active=user.is_active,
            name=user.name,
            last_name=user.last_name,
            full_name=user.full_name,
            pronoun=user.pronoun
        )


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User
