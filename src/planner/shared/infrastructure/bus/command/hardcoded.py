from src.planner.accounts.application.create.command import CreateAccountCommand
from src.planner.accounts.application.create.command_handler import (
    CreateAccountCommandHandler,
)
from src.planner.expenses.application.add.command import AddExpenseCommand
from src.planner.expenses.application.add.command_handler import (
    AddExpenseCommandHandler,
)
from src.planner.shared.domain.bus.command import Command
from src.planner.shared.domain.bus.command.exceptions import CommandNotRegistered
from src.planner.users.application.register.command import RegisterUserCommand
from src.planner.users.application.register.command_handler import (
    RegisterUserCommandHandler,
)


class HardcodedCommandBus:
    # TODO: Use dependency injection
    HANDLERS = {
        RegisterUserCommand: RegisterUserCommandHandler,
        CreateAccountCommand: CreateAccountCommandHandler,
        AddExpenseCommand: AddExpenseCommandHandler,
    }

    async def dispatch(self, command: Command) -> None:
        try:
            await self.HANDLERS[command.__class__]()(command)  # type: ignore[call-arg, arg-type, index] # noqa: E501
        except KeyError:
            raise CommandNotRegistered(command)
