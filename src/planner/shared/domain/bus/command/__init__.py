from typing import Protocol, runtime_checkable, ClassVar, Dict


@runtime_checkable
class Command(Protocol):
    __dataclass_fields__: ClassVar[Dict] 


@runtime_checkable
class CommandBus(Protocol):
    def dispatch(command: Command) -> None:
        ...


@runtime_checkable
class CommandHandler(Protocol):
    async def __call__(self, command: Command) -> None:
        ...
