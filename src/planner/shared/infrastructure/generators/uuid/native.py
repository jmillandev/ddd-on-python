from uuid import UUID, uuid4

from kink import inject

from src.planner.shared.domain.generators.uuid import UuidGenerator


@inject(alias=UuidGenerator)
class Uuid4Generator:
    def __call__(self) -> UUID:
        return uuid4()
