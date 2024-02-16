from kink import inject

from src.planner.shared.domain.users import UserId
from src.planner.users.domain.value_objects import (
    UserAvatar,
    UserLastName,
    UserName,
    UserPassword,
    UserPronoun,
)

from .command import UpdateUserAvatarCommand
from .avatar_updater import UserAvatarUpdater


@inject
class UpdateUserAvatarCommandHandler:
    def __init__(self, use_case: UserAvatarUpdater) -> None:
        self.use_case = use_case

    async def __call__(self, command: UpdateUserAvatarCommand) -> None:
        await self.use_case(
            id=UserId(command.id),
            avatar=UserAvatar.make(command.avatar),
            current_user_id=UserId(command.user_id)
        )
