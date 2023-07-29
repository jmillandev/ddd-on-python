from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class User(BaseModel):
    public_id: Optional[str] = None
    email: EmailStr
    is_active: Optional[bool] = True
    name: str
    last_name: str
