from kink import inject
from typing import Generic, Optional, TypeVar, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


from .models import Base
from src.shared.domain.value_objects.uuid import UuidValueObject
from src.shared.application.mappers import dict_to_entity

ModelType = TypeVar("ModelType", bound=Base)
Entity = TypeVar("Entity")


@inject
class SqlAlcheamyRepository(Generic[ModelType]):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    For more information on how to create new methods, see:
        https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
    """

    model_class: ModelType
    entity_class: Entity

    def __init__(self, session: async_sessionmaker[AsyncSession]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `session`: A SQLAlchemy database session object.
        """
        self.session = session


class SqlAlcheamyCreateMixin:

    async def create(self, user: Entity) -> Entity:
        user_object = self.model_class.from_entity(user)
        self.session.add(user_object)
        await self.session.commit()

class SqlAlcheamyFindMixin:

    async def find(self, id: UuidValueObject) -> Optional[Entity]:
        """Find object by id"""
        stmt = select(self.model_class).where(self.model_class.id == id.value).limit(1)
        return await self._find(stmt)

    async def _find(self, stmt: select) -> Optional[Entity]:
        """Find object by select statement"""
        result = await self.session.execute(stmt)
        data = result.scalars().first()
        if data:
            return dict_to_entity(data.to_dict(), self.entity_class)

class SqlAlcheamyGetAllMixin:

    async def all(self, skip: int = 0, limit: int = 10) -> Tuple[Entity]:
        # TODO: Create SkipValueObject and LimitValueObject
        stmt = select(self.model).offset(skip)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return (dict_to_entity(data.to_dict(), self.entity_class) for data in result.scalars().all())

    # TODO: Migrate method to async

    # def update(self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
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
