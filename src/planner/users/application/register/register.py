from kink import inject
from src.shared.domain.bus.event.event_bus import EventBus
from src.planner.shared.domain.users import UserId
from src.planner.users.domain.entity import User
from src.planner.users.domain.exceptions.email_already_used import EmailAlreadyUsed
from src.planner.users.domain.repository import UserRepository
from src.planner.users.domain.value_objects import (
    UserEmail,
    UserLastName,
    UserName,
    UserPassword,
    UserPronoun,
)


@inject
class UserRegistrator:
    def __init__(self, repository: UserRepository, event_bus: EventBus):
        self._repository = repository
        self._event_bus = event_bus

    async def create(
        self,
        id: UserId,
        email: UserEmail,
        name: UserName,
        last_name: UserLastName,
        pronoun: UserPronoun,
        password: UserPassword,
    ) -> User:
        user = await self._repository.search_by_email(email)
        # TODO: Use QueryBus instead Repository? https://pro.codely.com/library/cqrs-command-query-responsibility-segregation-29074/62554/path/step/33532843/discussion/79379/  # noqa:E501
        if user:
            raise EmailAlreadyUsed(email)

        user = User.create(id, email, name, last_name, pronoun, password)
        await self._repository.create(user)
        await self._event_bus.publish(*user.pull_domain_events())
        return user
