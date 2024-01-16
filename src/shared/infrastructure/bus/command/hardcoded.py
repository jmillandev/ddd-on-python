from src.shared.domain.bus.command import Command
from src.shared.domain.bus.command.exceptions import CommandNotRegistered
from src.users.application.command_handler import CreateUserCommand, CreateUserCommandHandler

class HardcodedCommandBus:

    HANDLERS = {
        CreateUserCommand: CreateUserCommandHandler
    }

    async def dispatch(self, command: Command)-> None:
        try:
            await self.HANDLERS[command.__class__]()(command)
        except KeyError:
            raise CommandNotRegistered(command)
