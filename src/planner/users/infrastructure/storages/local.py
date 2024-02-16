from src.planner.shared.domain.value_objects.file import FileValueObject
from kink import inject
from src.planner.users.domain.storage import UserFileStorage
from pathlib import Path

@inject(use_factory=True, alias=UserFileStorage)
class LocalUserFileStorage:

    def __init__(self, basedir: str = 'files') -> None:
        self._basedir = basedir
        

    async def push(self, file: bytes, path: str) -> None:
        Path(f"{self._basedir}/{path}").parent.mkdir(parents=True, exist_ok=True)
        with open(f"{self._basedir}/{path}", "wb") as f:
            f.write(file)

    async def pull(self, path: str) -> bytes:
        with open(f"{self._basedir}/{path}", "rb") as f:
            response = f.read()
        return response
