from uuid import UUID, uuid4

class Uuid4Generator:
    def __call__(self) -> UUID:
        return uuid4()