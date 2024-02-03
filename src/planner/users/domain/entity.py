from typing import Self

from src.planner.shared.domain.aggregates import AggregateRoot, aggregate_dataclass
from src.planner.shared.domain.users import UserId
from src.planner.shared.domain.users.events import UserRegistered
from src.planner.users.domain.value_objects import (
    UserCreatedAt,
    UserEmail,
    UserIsActive,
    UserLastName,
    UserName,
    UserPassword,
    UserPronoun,
)


@aggregate_dataclass
class User(AggregateRoot):
    id: UserId
    created_at: UserCreatedAt
    email: UserEmail
    name: UserName
    last_name: UserLastName
    is_active: UserIsActive
    pronoun: UserPronoun
    password: UserPassword

    def __str__(self) -> str:
        return f"User(id={self.id}, email={self.email})"

    @classmethod
    def register(
        cls,
        id: UserId,
        email: UserEmail,
        name: UserName,
        last_name: UserLastName,
        pronoun: UserPronoun,
        password: UserPassword,
    ) -> Self:
        user = cls(
            id=id,
            created_at=UserCreatedAt.now(),
            email=email,
            name=name,
            last_name=last_name,
            is_active=UserIsActive(True),
            pronoun=pronoun,
            password=password,
        )
        user._record_event(
            UserRegistered.make(
                user.id.primitive,
                ocurrend_at=user.created_at.primitive,
                email=user.email.primitive,
                pronoun=user.pronoun.primitive,
                name=user.name.primitive,
                last_name=user.last_name.primitive,
            )
        )
        return user
