from typing import Generic, Optional, TypeVar

from kink import inject
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.planner.shared.application.mappers import dict_to_entity
from src.planner.shared.domain.aggregates import AggregateRoot
from src.planner.shared.domain.value_objects.uuid import UuidValueObject

from .models import Base

ModelType = TypeVar("ModelType", bound=Base)
Aggregate = TypeVar("Aggregate", bound=AggregateRoot)


@inject
class SqlAlchemyRepository(Generic[ModelType, Aggregate]):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    For more information on how to create new methods, see:
        https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
    """

    model_class: ModelType
    entity_class: type[Aggregate]

    def __init__(self, sqlalchemy_sessionmaker: type[AsyncSession]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `sqlalchemy_sessionmaker`: A SQLAlchemy database session object.
        """
        self.sessionmaker = sqlalchemy_sessionmaker


class SqlAlchemyCreateMixin(Generic[ModelType]):
    sessionmaker: type[AsyncSession]
    model_class: ModelType

    async def create(self, entity: Aggregate) -> None:
        entity_object = self.model_class.from_entity(entity)
        async with self.sessionmaker() as session:
            session.add(entity_object)
            await session.commit()
        return None


class SqlAlchemySaveMixin(Generic[ModelType]):
    sessionmaker: type[AsyncSession]
    model_class: ModelType

    async def save(self, entity: Aggregate) -> None:
        entity_object = self.model_class.from_entity(entity)
        async with self.sessionmaker() as session:
            await session.merge(entity_object)
            await session.commit()


class SqlAlchemySearchMethodMixin(Generic[Aggregate]):
    sessionmaker: type[AsyncSession]
    entity_class: type[Aggregate]

    async def _search(self, stmt: Select) -> Optional[Aggregate]:
        """Search object by select statement"""
        async with self.sessionmaker() as session:
            result = await session.execute(stmt)
        data = result.scalars().first()
        if data:
            return dict_to_entity(data.to_dict(), self.entity_class)
        return None


class SqlAlchemyFindMixin(SqlAlchemySearchMethodMixin, Generic[Aggregate]):
    sessionmaker: type[AsyncSession]
    entity_class: type[Aggregate]

    async def search(self, id: UuidValueObject) -> Optional[Aggregate]:
        """Search object by id"""
        stmt = select(self.model_class).where(self.model_class.id == id.value).limit(1)  # type: ignore[attr-defined] # noqa: E501
        return await self._search(stmt)


# class SqlAlchemyGetAllMixin:
#     async def all(self, skip: int = 0, limit: int = 10) -> Tuple[Aggregate]:
# TODO: Use criteria instead offset and limit
# TODO: Create SkipValueObject and LimitValueObject
# stmt = select(self.model).offset(skip)
# if limit is not None:
#     stmt = stmt.limit(limit)
# result = await self.sessionmaker.execute(stmt)
# return tuple(
#     dict_to_entity(data.to_dict(), self.entity_class)
#     for data in result.scalars().all()
# )

# TODO: Migrate method to async

# def update(self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:  # noqa: E501
#     obj_data = jsonable_encoder(db_obj)
#     if isinstance(obj_in, dict):
#         update_data = obj_in
#     else:
#         update_data = obj_in.dict(exclude_unset=True)
#     for field in obj_data:
#         if field in update_data:
#             setattr(db_obj, field, update_data[field])
#     self.db.add(db_obj)
#     self.db.commit()
#     self.db.refresh(db_obj)
#     return db_obj

# def remove(self, *, id: int) -> ModelType:
#     obj = self.db.query(self.model).get(id)
#     self.db.delete(obj)
#     self.db.commit()
#     return obj
