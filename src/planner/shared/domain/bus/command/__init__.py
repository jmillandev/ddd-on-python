from typing import ClassVar, Dict, Protocol, runtime_checkable


@runtime_checkable
class Command(Protocol):
    # TODO: Change to Abstract Class
    __dataclass_fields__: ClassVar[Dict]

    @classmethod
    def from_dict(cls, data: dict):
        attributes = {key: data[key] for key in cls.__annotations__.keys()}
        return cls(**attributes)


@runtime_checkable
class CommandBus(Protocol):
    async def dispatch(self, command: Command) -> None:
        ...


@runtime_checkable
class CommandHandler(Protocol):
    async def __call__(self, command: Command) -> None:
        ...
