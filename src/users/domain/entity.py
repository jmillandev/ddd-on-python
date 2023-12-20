from src.users.domain.value_objects import (UserCreatedAt, UserEmail, UserId,
                                            UserIsActive, UserLastName,
                                            UserName, UserPassword,
                                            UserPronoun)


class User:
    id: UserId
    created_at: UserCreatedAt
    email: UserEmail
    name: UserName
    last_name: UserLastName
    is_active: UserIsActive
    pronoun: UserPronoun
    password: UserPassword

    def __init__(self, id: UserId, created_at: UserCreatedAt, email: UserEmail, name: UserName,
                 last_name: UserLastName, is_active: UserIsActive, pronoun: UserPronoun,
                 password: UserPassword) -> None:
        self.id = id
        self.created_at = created_at
        self.email = email
        self.name = name
        self.last_name = last_name
        self.is_active = is_active
        self.pronoun = pronoun
        self.password = password

    @classmethod
    def create(self, id: UserId, email: UserEmail, name: UserName, last_name: UserLastName, pronoun: UserPronoun, password: UserPassword):
        user = User(
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