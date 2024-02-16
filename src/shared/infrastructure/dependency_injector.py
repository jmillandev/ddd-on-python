"""All infrastructure dependencies should be imported here. This file is used to
initialize the dependency injector.

Infracstructure dependencies need to be imported here for python interpreter to know about
them. This is necessary because the dependency injector uses the `importlib` module to
import the dependencies.
"""

from importlib import import_module
from pathlib import Path
from typing import Set

from kink import Container, di
from motor.core import AgnosticDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.planner.accounts.infrastructure.repositories.sqlalchemy import (  # noqa: F401
    SqlAlchemyAccountRepository,
)
from src.planner.auth_token.infrastructure.encoders.jose_jwt import (  # noqa: F401
    JoseJwtEncoder,
)
from src.planner.auth_token.infrastructure.repositories.sqlalchemy import (  # noqa: F401
    SqlAlchemyAuthCredentialRepository,
)
from src.planner.movements.infrastructure.repositories.motor import (  # noqa: F401
    MotorMovementRepository,
)
from src.planner.shared.infrastructure.bus.command.hardcoded import (  # noqa: F401
    HardcodedCommandBus,
)
from src.planner.shared.infrastructure.bus.query.hardcoded import (  # noqa: F401
    HardcodedQueryBus,
)
from src.planner.shared.infrastructure.encryptors.unidirectionals.bcrypt import (  # noqa: F401
    BcryptUnidirectionalEncryptor,
)
from src.planner.shared.infrastructure.generators.uuid.native import (  # noqa: F401
    Uuid4Generator,
)
from src.planner.shared.infrastructure.persistence.motor.db import database
from src.planner.shared.infrastructure.persistence.sqlalchemy.session import (
    SqlAlchemySession,
)
from src.planner.users.infrastructure.repositories.sqlalchemy import (  # noqa: F401
    SqlAlchemyUserRepository,
)
from src.shared.domain.bus.event.domain_event_susbcriber import DomainEventSubscriber
from src.shared.infrastructure.bus.event.in_memory.event_bus import (  # noqa: F401
    InMemoryEventBus,
)


def search_subscribers() -> Set[type[DomainEventSubscriber]]:
    for module_name in Path(".").glob("src/**/application/*/subscribers"):
        import_module(str(module_name).replace("/", "."))

    return set(DomainEventSubscriber.__subclasses__())


def init(dependency_injector: Container = di) -> None:
    dependency_injector.factories[type[AsyncSession]] = lambda _: SqlAlchemySession  # type: ignore[misc]  # noqa: E501
    # TODO: I'm not sure if this is the best way. Maybe this will to create a
    # new connection every time it's called
    dependency_injector.factories[AgnosticDatabase] = lambda _: database()
    dependency_injector[Set[type[DomainEventSubscriber]]] = search_subscribers()
