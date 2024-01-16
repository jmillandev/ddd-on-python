from kink import inject

from src.shared.domain.users import UserId
from src.users.domain.entity import User
from src.users.domain.exceptions.email_already_used import EmailAlreadyUsed
from src.users.domain.repository import UserRepository
from src.users.domain.value_objects import (UserEmail, UserLastName, UserName,
                                            UserPassword, UserPronoun)


@inject
class UserCreator:
    def __init__(self, repository: UserRepository):
        self._repository = repository
        # TODO-Events: add event bus
        # self._event_bus = EventBus()

    async def create(self, id: UserId, email: UserEmail, name: UserName, last_name: UserLastName, pronoun: UserPronoun, password: UserPassword) -> User:
        user = await self._repository.search_by_email(email)
        # TODO: Use QueryBus instead Repository? https://pro.codely.com/library/cqrs-command-query-responsibility-segregation-29074/62554/path/step/33532843/discussion/79379/
        if user:
            raise EmailAlreadyUsed(email)

        user = User.create(id, email, name, last_name, pronoun, password)
        await self._repository.create(user)
        # TODO-Events: publish events
        # self._event_bus.publish(*user.pull_domain_events())
        return user
