from dataclasses import dataclass
from typing import Any

from src.shared.domain.users import UserId
from src.users.domain.value_objects import (UserCreatedAt, UserEmail,
                                            UserIsActive, UserLastName,
                                            UserName, UserPassword,
                                            UserPronoun)


@dataclass
class User:
    id: UserId
    created_at: UserCreatedAt
    email: UserEmail
    name: UserName
    last_name: UserLastName
    is_active: UserIsActive
    pronoun: UserPronoun
    password: UserPassword

    @classmethod
    def create(cls, id: UserId, email: UserEmail, name: UserName, last_name: UserLastName, pronoun: UserPronoun, password: UserPassword):
        user = cls(
            id=id,
            created_at=UserCreatedAt.now(),
            email=email,
            name=name,
            last_name=last_name,
            is_active=UserIsActive(True),
            pronoun=pronoun,
            password=password
        )
        # TODO-Events: register event
        # user._register_event(UserCreated(user))
        return user

    def pull_domain_events(self):
        # TODO-Events: return events
        # events = self._domain_events
        # self._domain_events = []
        # return events
        pass

    # TODO-Events: append event
    # def _register_event(self, event: DomainEvent):
        # self._domain_events.append(event)

    def __str__(self) -> str:
        return f"[{self.id}] {self.full_name}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}('{(self)}')>"

    @property
    def full_name(self):
        return f"{self.name} {self.last_name}".strip()

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, User):
            return False
        return self.id == o.id

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """Create a User from a dict.
        Used for deserialization of a User.

        Args:
            data (dict[str, Any]): A dict with the attributes of a User.

        Returns:
            User
        """
        annotations = cls.__annotations__
        attributes = { key: annotations[key](value) for key, value in data.items() if key in annotations }
        return cls(**attributes)
