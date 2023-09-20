from typing import Optional

from pydantic import BaseModel, EmailStr
from apps.users.types import Pronoun

# Shared properties
class User(BaseModel):
    public_id: Optional[str] = None
    email: EmailStr
    is_active: Optional[bool] = True
    name: str
    last_name: str
    pronoun: Optional[Pronoun]
