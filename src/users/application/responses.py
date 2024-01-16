from src.shared.application.response import Response
from src.users.domain.value_objects.pronoun import Pronoun


class UserResponse(Response):
    id: str
    email: str
    name: str
    last_name: str
    pronoun: Pronoun
