from src.users.domain.value_objects import (UserCreatedAt, UserEmail, UserId,
                                            UserIsActive, UserLastName,
                                            UserName, UserPassword,
                                            UserPronoun, UserUpdatedAt)


class User:
    id: UserId
    created_at: UserCreatedAt
    updated_at: UserUpdatedAt
    email: UserEmail
    name: UserName
    last_name: UserLastName
    is_active: UserIsActive
    pronoun: UserPronoun
    password: UserPassword

    def __init__(self, id: UserId, created_at: UserCreatedAt, updated_at: UserUpdatedAt,
                 email: UserEmail, name: UserName, last_name: UserLastName, is_active: UserIsActive,
                 pronoun: UserPronoun, password: UserPassword) -> None:
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.email = email
        self.name = name
        self.last_name = last_name
        self.is_active = is_active
        self.pronoun = pronoun
        self.password = password

    def __str__(self) -> str:
        return f"[{self.id}] {self.full_name}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}('{(self)}')>"

    @property
    def full_name(self):
        return f"{self.name} {self.last_name}".strip()
