from kink import inject

from src.planner.shared.domain.users import UserId
from src.planner.users.domain.value_objects import (
    UserEmail,
    UserLastName,
    UserName,
    UserPassword,
    UserPronoun,
)

from .command import RegisterUserCommand
from .register import UserRegistrator


@inject
class RegisterUserCommandHandler:
    def __init__(self, creator: UserRegistrator) -> None:
        self.creator = creator

    async def __call__(self, command: RegisterUserCommand) -> None:
        await self.creator.create(
            id=UserId(command.id),
            email=UserEmail(command.email),
            name=UserName(command.name),
            last_name=UserLastName(command.last_name),
            pronoun=UserPronoun(command.pronoun),
            password=UserPassword(command.password),  # type: ignore[call-arg]
        )
