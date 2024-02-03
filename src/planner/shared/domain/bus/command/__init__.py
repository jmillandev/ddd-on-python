from abc import ABCMeta, abstractmethod
from typing import Protocol, runtime_checkable, Union, Dict

Primitive = Union[str, int, bool]

class Command(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self) -> None:
        """Overwrite this methos using @dataclass"""

    @classmethod
    def from_dict(cls, data: Dict[str, Primitive]) -> "Command":
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
