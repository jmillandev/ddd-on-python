from kink import di
from sqlalchemy.ext.asyncio import AsyncSession

from src.planner.accounts.application.create.creator import AccountCreator
from src.planner.accounts.application.find.finder import AccountFinder
from src.planner.accounts.domain.repository import AccountRepository
from src.planner.accounts.infrastructure.repositories.sqlalchemy import (
    SqlAlchemyAccountRepository,
)
from src.planner.auth_token.application.create.creator import AuthTokenCreator
from src.planner.auth_token.domain.encoder import AuthEncoder
from src.planner.auth_token.domain.repository import AuthCredentialRepository
from src.planner.auth_token.infrastructure.encoders.jose_jwt import JoseJwtEncoder
from src.planner.auth_token.infrastructure.repositories.sqlalchemy import (
    SqlAlchemyAuthCredentialRepository,
)
from src.planner.movements.application.expenses.add.adder import ExpenseMovementAdder
from src.planner.movements.domain.repository import MovementRepository
from src.planner.movements.infrastructure.repositories.sqlalchemy import (
    SqlAlchemyMovementRepository,
)
from src.planner.shared.domain.bus.command import CommandBus
from src.planner.shared.domain.bus.query import QueryBus
from src.planner.shared.domain.encryptors.unidirectional import UnidirectionalEncryptor
from src.planner.shared.domain.generators.uuid import UuidGenerator
from src.planner.shared.infrastructure.bus.command.hardcoded import HardcodedCommandBus
from src.planner.shared.infrastructure.bus.query.hardcoded import HardcodedQueryBus
from src.planner.shared.infrastructure.encryptors.unidirectionals.bcrypt import (
    BcryptUnidirectionalEncryptor,
)
from src.planner.shared.infrastructure.generators.uuid.native import Uuid4Generator
from src.planner.shared.infrastructure.persistence.sqlalchemy.session import (
    SqlAlchemySession,
)
from src.planner.users.application.register.register import UserRegistrator
from src.planner.users.domain.repository import UserRepository
from src.planner.users.infrastructure.repositories.sqlalchemy import (
    SqlAlchemyUserRepository,
)
from src.shared.domain.bus.event.event_bus import EventBus

from .event_bus import start_event_bus


def init():
    di.factories[AsyncSession] = lambda _: SqlAlchemySession()
    di[CommandBus] = HardcodedCommandBus()
    di[QueryBus] = HardcodedQueryBus()
    di[EventBus] = start_event_bus()
    di[UuidGenerator] = Uuid4Generator()

    # Auth
    di[AuthEncoder] = JoseJwtEncoder()
    di.factories[AuthTokenCreator] = lambda _: AuthTokenCreator()
    di.factories[
        AuthCredentialRepository
    ] = lambda _: SqlAlchemyAuthCredentialRepository()
    # Accounts
    di.factories[AccountCreator] = lambda _: AccountCreator()
    di.factories[AccountFinder] = lambda _: AccountFinder()
    di.factories[AccountRepository] = lambda _: SqlAlchemyAccountRepository()

    # Expenses
    di.factories[MovementRepository] = lambda _: SqlAlchemyMovementRepository()
    di.factories[ExpenseMovementAdder] = lambda _: ExpenseMovementAdder()

    # Users
    di.factories[UserRepository] = lambda _: SqlAlchemyUserRepository()
    di.factories[UserRegistrator] = lambda _: UserRegistrator()
    di[UnidirectionalEncryptor] = BcryptUnidirectionalEncryptor()
