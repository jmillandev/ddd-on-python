from kink import di
from sqlalchemy.ext.asyncio import AsyncSession

from src.planner.auth_token.application.create.creator import AuthTokenCreator
from src.planner.auth_token.domain.encoder import AuthEncoder
from src.planner.auth_token.domain.repository import AuthCredentialRepository
from src.planner.auth_token.infrastructure.encoders.jose_jwt import JoseJwtEncoder
from src.planner.auth_token.infrastructure.repositories.sqlalchemy import (
    SqlAlcheamyAuthCredentialRepository,
)
from src.planner.shared.domain.bus.command import CommandBus
from src.planner.shared.domain.bus.query import QueryBus
from src.planner.shared.domain.encryptors.unidirectional import UnidirectionalEncryptor
from src.planner.shared.infrastructure.bus.command.hardcoded import HardcodedCommandBus
from src.planner.shared.infrastructure.bus.query.hardcoded import HardcodedQueryBus
from src.planner.shared.infrastructure.encryptors.unidirectionals.bcrypt import (
    BcryptUnidirectionalEncryptor,
)
from src.planner.shared.infrastructure.persistence.sqlalchemy.session import (
    SqlAlchemySession,
)
from src.planner.users.application.register.register import UserRegistrator
from src.planner.users.domain.repository import UserRepository
from src.planner.users.infrastructure.repositories.sqlalchemy import (
    SqlAlcheamyUserRepository,
)
from src.shared.domain.bus.event.event_bus import EventBus

from .event_bus import start_event_bus


def init():
    di.factories[AsyncSession] = lambda _: SqlAlchemySession()
    di.factories[UserRepository] = lambda _: SqlAlcheamyUserRepository()
    di.factories[
        AuthCredentialRepository
    ] = lambda _: SqlAlcheamyAuthCredentialRepository()
    di.factories[UserRegistrator] = lambda _: UserRegistrator()
    di.factories[AuthTokenCreator] = lambda _: AuthTokenCreator()
    di[UnidirectionalEncryptor] = BcryptUnidirectionalEncryptor()
    di[CommandBus] = HardcodedCommandBus()
    di[AuthEncoder] = JoseJwtEncoder()
    di[QueryBus] = HardcodedQueryBus()
    di[EventBus] = start_event_bus()
