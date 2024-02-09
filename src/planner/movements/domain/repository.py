from typing import Protocol, runtime_checkable

from .aggregate import Movement


@runtime_checkable
class MovementRepository(Protocol):
    # TODO: Use save in other repositories
    async def save(self, movement: Movement) -> None:
        ...

    async def search(self, id: str) -> Movement:
        ...
