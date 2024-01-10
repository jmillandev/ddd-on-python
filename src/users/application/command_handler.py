from kink import inject

from src.shared.domain.users import UserId
from src.users.domain.value_objects import (UserEmail, UserLastName, UserName,
                                            UserPassword, UserPronoun)

from .command import CreateUserCommand
from .creator import UserCreator


@inject
class CreateUserCommandHandler:

    def __init__(self, creator: UserCreator) -> None:
        self.creator = creator

    async def __call__(self, command: CreateUserCommand) -> None:
        await self.creator.create(
            id=UserId(command.id),
            email=UserEmail(command.email),
            name=UserName(command.name),
            last_name=UserLastName(command.last_name),
            pronoun=UserPronoun(command.pronoun),
            password=UserPassword(command.password)
        )
