from uuid import UUID
from typing import Protocol


class UuidGenerator(Protocol):
    def __call__(self) -> UUID:
        ...
