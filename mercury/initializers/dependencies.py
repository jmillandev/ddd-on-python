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
from src.shared.domain.bus.query import QueryBus
from src.shared.infrastructure.bus.query.hardcoded import HardcodedQueryBus

def init():
    di.factories[AsyncSession] = lambda _: SqlAlchemySession()
    di.factories[UserRepository] = lambda _: SqlAlcheamyUserRepository()
    di.factories[AuthCredentialRepository] = lambda _: SqlAlcheamyAuthCredentialRepository()
    di.factories[UserCreator] = lambda _: UserCreator()
    di.factories[AuthTokenCreator] = lambda _: AuthTokenCreator()
    di[UnidirectionalEncryptor] = PasslibUnidirectionalEncryptor()
    di[CommandBus] = HardcodedCommandBus()
    di[AuthEncoder] = JoseJwtEncoder()
    di[QueryBus] = HardcodedQueryBus()
