from kink import inject

from src.planner.shared.domain.users import UserId
from src.planner.users.domain.repository import UserRepository
from src.planner.users.domain.value_objects import UserAvatar
from src.shared.domain.bus.event.event_bus import EventBus
from src.planner.users.application.find.finder import UserFinder


@inject(use_factory=True)
class UserAvatarUpdater:
    def __init__(self, 
                 repository: UserRepository,
                 event_bus: EventBus,
                 user_finder: UserFinder
                 ):
        self._repository = repository
        self._event_bus = event_bus
        self._user_finder = user_finder

    async def __call__(
        self,
        id: UserId,
        current_user_id: UserId,
        avatar: UserAvatar,
    ) -> None:
        user = await self._user_finder(id, current_user_id)
        await user.update_avatar(avatar)
        await self._repository.save(user)
        await self._event_bus.publish(*user.pull_domain_events())
