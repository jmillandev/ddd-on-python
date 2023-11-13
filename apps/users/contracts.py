from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr

from src.users.domain.value_objects.pronoun import Pronoun


class UserCreateContract(BaseModel):
    # TODO: Create a contract base on the User entity
    email: EmailStr
    name: str
    last_name: str
    password: str
    pronoun: Pronoun


class GranType(str, Enum):
    password = 'password'


class OAuth2Contract(BaseModel):
    """
        It creates the following Form request parameters in your endpoint:

    grant_type: the OAuth2 spec says it is required and MUST be the fixed string "password".
        Nevertheless, this dependency class is permissive and allows not passing it. If you want to enforce it,
        use instead the OAuth2PasswordRequestFormStrict dependency.
    username: username string. The OAuth2 spec requires the exact field name "username".
    password: password string. The OAuth2 spec requires the exact field name "password".
    scope: Optional string. Several scopes (each one a string) separated by spaces. E.g.
        "items:read items:write users:read profile openid"
    client_id: optional string. OAuth2 recommends sending the client_id and client_secret (if any)
        using HTTP Basic auth, as: client_id:client_secret
    client_secret: optional string. OAuth2 recommends sending the client_id and client_secret (if any)
        using HTTP Basic auth, as: client_id:client_secret
    """

    username: str
    password: str
    grant_type: GranType
    scope: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None