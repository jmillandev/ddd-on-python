from kink import di
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.shared.domain.bus.command import CommandBus
from src.shared.infrastructure.bus.command.hardcoded import HardcodedCommandBus
from src.users.application.creator import UserCreator
from src.users.domain.repository import UserRepository
from src.users.infrastructure.repositories.sqlalchemy import SqlAlcheamyUserRepository

def init():
    di[CommandBus] = HardcodedCommandBus()
    di[UserRepository] = lambda di: SqlAlcheamyUserRepository()
    di[UserCreator] = lambda di: UserCreator()