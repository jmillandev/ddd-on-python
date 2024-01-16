from kink import di
from sqlalchemy.ext.asyncio import AsyncSession

from src.planner.shared.infrastructure.persistence.sqlalchemy.session import SqlAlchemySession
from src.planner.auth.application.creator import AuthTokenCreator
from src.planner.auth.domain.encoder import AuthEncoder
from src.planner.auth.domain.repository import AuthCredentialRepository
from src.planner.auth.infrastructure.encoders.jose_jwt import JoseJwtEncoder
from src.planner.auth.infrastructure.repositories.sqlalchemy import \
    SqlAlcheamyAuthCredentialRepository
from src.planner.shared.domain.bus.command import CommandBus
from src.planner.shared.domain.encryptors.unidirectional import UnidirectionalEncryptor
from src.planner.shared.infrastructure.bus.command.hardcoded import HardcodedCommandBus
from src.planner.shared.infrastructure.encryptors.unidirectionals.passlib import \
    PasslibUnidirectionalEncryptor
from src.planner.users.application.creator import UserCreator
from src.planner.users.domain.repository import UserRepository
from src.planner.users.infrastructure.repositories.sqlalchemy import \
    SqlAlcheamyUserRepository
from src.planner.shared.domain.bus.query import QueryBus
from src.planner.shared.infrastructure.bus.query.hardcoded import HardcodedQueryBus

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
