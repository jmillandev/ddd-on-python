from kink import di
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.shared.domain.bus.command import CommandBus
from src.shared.infrastructure.bus.command.hardcoded import HardcodedCommandBus
from src.users.application.creator import UserCreator
from src.users.domain.repository import UserRepository
from src.users.infrastructure.repositories.sqlalchemy import SqlAlcheamyUserRepository
from src.auth.domain.repository import AuthCredentialRepository
from src.auth.infrastructure.repositories.sqlalchemy import SqlAlcheamyAuthCredentialRepository
from src.auth.domain.encoder import AuthEncoder
from src.auth.infrastructure.encoders.jose_jwt import JoseJwtEncoder
from src.shared.domain.encryptors.unidirectional import UnidirectionalEncryptor
from src.shared.infrastructure.encryptors.unidirectionals.passlib import PasslibUnidirectionalEncryptor


def init():
    di[CommandBus] = HardcodedCommandBus()
    di[AuthEncoder] = JoseJwtEncoder()
    di[UserRepository] = lambda di: SqlAlcheamyUserRepository()
    di[AuthCredentialRepository] = lambda di: SqlAlcheamyAuthCredentialRepository()
    di[UserCreator] = lambda di: UserCreator()
    di[UnidirectionalEncryptor] = PasslibUnidirectionalEncryptor()