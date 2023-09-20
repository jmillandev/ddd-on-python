from pydantic import BaseModel, EmailStr
from apps.users.types import Pronoun

class UserCreateContract(BaseModel):
    email: EmailStr
    name: str
    last_name: str
    password: str
    pronoun: Pronoun
