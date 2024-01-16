from kink import di
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.persistence.sqlalchemy.session import SqlAlchemySession
from src.auth.application.creator import AuthTokenCreator
from src.auth.domain.encoder import AuthEncoder
from src.auth.domain.repository import AuthCredentialRepository
from src.auth.infrastructure.encoders.jose_jwt import JoseJwtEncoder
from src.auth.infrastructure.repositories.sqlalchemy import \
    SqlAlcheamyAuthCredentialRepository
from src.shared.domain.bus.command import CommandBus
from src.shared.domain.encryptors.unidirectional import UnidirectionalEncryptor
from src.shared.infrastructure.bus.command.hardcoded import HardcodedCommandBus
from src.shared.infrastructure.encryptors.unidirectionals.passlib import \
    PasslibUnidirectionalEncryptor
from src.users.application.creator import UserCreator
from src.users.domain.repository import UserRepository
from src.users.infrastructure.repositories.sqlalchemy import \
    SqlAlcheamyUserRepository


def init():
    di[AsyncSession] = lambda _: SqlAlchemySession()
    di[CommandBus] = HardcodedCommandBus()
    di[AuthEncoder] = JoseJwtEncoder()
    di[UserRepository] = lambda _: SqlAlcheamyUserRepository()
    di[AuthCredentialRepository] = lambda _: SqlAlcheamyAuthCredentialRepository()
    di[UserCreator] = lambda _: UserCreator()
    di[UnidirectionalEncryptor] = PasslibUnidirectionalEncryptor()
    di[AuthTokenCreator] = lambda _: AuthTokenCreator()
