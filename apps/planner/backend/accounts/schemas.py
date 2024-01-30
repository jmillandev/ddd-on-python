from dataclasses import asdict, dataclass

from src.planner.accounts.application.create.command import CreateAccountCommand


@dataclass(frozen=True)
class CreateAccountSchema:
    __annotations__ = {
        key: value
        for key, value in CreateAccountCommand.__annotations__.items()
        if key not in ["id", "user_id"]
    }

    def to_dict(self):
        return asdict(self)
