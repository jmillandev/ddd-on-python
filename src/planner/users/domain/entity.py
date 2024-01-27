from dataclasses import dataclass
from typing import List
from src.shared.domain.bus.event.domain_event import DomainEvent
from src.planner.shared.domain.users import UserId
from src.planner.users.domain.value_objects import (
    UserCreatedAt,
    UserEmail,
    UserIsActive,
    UserLastName,
    UserName,
    UserPassword,
    UserPronoun,
)
from src.planner.users.domain.events.registered import UserRegistered

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
    def register(
        cls,
        id: UserId,
        email: UserEmail,
        name: UserName,
        last_name: UserLastName,
        pronoun: UserPronoun,
        password: UserPassword,
    ):
        user = cls(
            id=id,
            created_at=UserCreatedAt.now(),
            email=email,
            name=name,
            last_name=last_name,
            is_active=UserIsActive(True),
            pronoun=pronoun,
            password=password,
        )
        user._record_event(
            UserRegistered.make(
                user.id.value,
                ocurrend_at=user.created_at.primitive,
                email=user.email.primitive,
                pronoun=user.pronoun.primitive,
                name=user.name.primitive,
                last_name=user.last_name.primitive,
            )
        )
        return user

    def pull_domain_events(self) -> List[DomainEvent]:
        # TODO: Move to AggregateRoot
        events = self._recorded_events
        self.__recorded_events = []
        return events

    def _record_event(self, event: DomainEvent):
        # TODO: Move to AggregateRoot
        self._recorded_events.append(event)

    def __str__(self) -> str:
        return f"[{self.id}] {self.email}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}('{(self)}')>"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, User):
            return False
        return self.id == o.id

    @property
    def _recorded_events(self) -> List[DomainEvent]:
        # TODO: Move to AggregateRoot
        if not hasattr(self, "__recorded_events"): self.__recorded_events = []
        return self.__recorded_events
