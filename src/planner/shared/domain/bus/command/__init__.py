from typing import Protocol, runtime_checkable


@runtime_checkable
class Command(Protocol):
    """Is DTO to

    Args:
        Protocol (_type_): _description_
    """


@runtime_checkable
class CommandBus(Protocol):
    def dispatch(command: Command) -> None:
        ...


@runtime_checkable
class CommandHandler(Protocol):
    async def __call__(self, command: Command) -> None:
        ...
