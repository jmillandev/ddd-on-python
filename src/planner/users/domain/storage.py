from typing import Protocol, runtime_checkable


@runtime_checkable
class UserFileStorage(Protocol):
    async def push(self, file: bytes, path: str) -> None:
        ...

    async def pull(self, path: str) -> None:
        ...

    def url(self, path: str) -> str:
        ...
