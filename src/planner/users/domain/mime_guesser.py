from typing import Protocol, runtime_checkable


@runtime_checkable
class MimeGuesser(Protocol):
    def extension(self, file: bytes) -> str:
        ...
