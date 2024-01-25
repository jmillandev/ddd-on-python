from src.planner.shared.domain.bus.command import Command
from src.planner.shared.domain.bus.command.exceptions import CommandNotRegistered
from src.planner.users.application.create.command_handler import (
    CreateUserCommand,
    CreateUserCommandHandler,
)


class HardcodedCommandBus:
    HANDLERS = {CreateUserCommand: CreateUserCommandHandler}

    async def dispatch(self, command: Command) -> None:
        try:
            await self.HANDLERS[command.__class__]()(command)  # type: ignore[call-arg, arg-type, index] # noqa: E501
        except KeyError:
            raise CommandNotRegistered(command)
