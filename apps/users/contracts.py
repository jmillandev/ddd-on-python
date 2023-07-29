from pydantic import BaseModel, EmailStr


class UserCreateContract(BaseModel):
    email: EmailStr
    name: str
    last_name: str
    password: str
