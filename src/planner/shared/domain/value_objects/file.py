from src.planner.shared.domain.value_objects.base import ValueObject
from typing import Any, Self

from uuid import uuid4
from src.planner.users.domain.storage import UserFileStorage
from src.planner.users.domain.mime_guesser import MimeGuesser
from kink import inject

@inject
class FileValueObject(ValueObject):

    BASE_TYPE = bytes
    SUBPATH = str

    def __init__(self, value: Any, filename: str, storage: UserFileStorage) -> None:
        """
        Args:
            value (str): Filename
            content (bytes, optional): FileContent
        """
        self._filename = filename
        self._storage = storage
        super().__init__(value)

    @property
    def filename(self)-> str:
        return self._filename

    @classmethod
    @inject
    def make(cls, file, mime_guesser: MimeGuesser) -> Self:
        filename = f"{uuid4()}{mime_guesser.extension(file)}"
        return cls(file, filename)

    async def push(self) -> None:
        await self._storage.push(self.value, self.SUBPATH + self.filename)
