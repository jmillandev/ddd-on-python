from src.users.domain.repository import UserRepository
from src.users.domain.entity import User
from src.users.domain.value_objects import UserId, UserEmail, UserLastName, UserName, UserPassword, UserPronoun


class UserCreator:
    def __ini__(self, repository: UserRepository):
        self._repository = repository
        # TODO-Events: add event bus
        # self._event_bus = EventBus()

        async def create(self, id: UserId, email: UserEmail, name: UserName, last_name: UserLastName, pronoun: UserPronoun, password: UserPassword) -> User:
            user = User.create(id, email, name, last_name, pronoun, password)
            await self._repository.create(user)
            # TODO-Events: publish events
            # self._event_bus.publish(*user.pull_domain_events())
            return user
