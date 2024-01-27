from typing import Optional
from uuid import uuid4

from faker import Faker

from src.planner.auth_token.domain.entity import AuthCredential
from src.planner.shared.application.mappers import dict_to_entity

fake = Faker()


class AuthCredentialFactory:
    @classmethod
    def build(cls, **kwargs) -> AuthCredential:
        return dict_to_entity(cls.to_dict(**kwargs), AuthCredential)

    @staticmethod
    def to_dict(
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> dict:
        return {
            "user_id": user_id or uuid4(),
            "username": username or fake.email(),
            "password": password or fake.password(),
        }