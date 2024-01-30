from typing import Protocol
from uuid import UUID


class UuidGenerator(Protocol):
    def __call__(self) -> UUID:
        ...
