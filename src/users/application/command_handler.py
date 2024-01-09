from kink import inject
from .command import CreateUserCommand
from .creator import UserCreator
from src.users.domain.value_objects import UserId, UserEmail, UserLastName, UserName, UserPassword, UserPronoun


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
