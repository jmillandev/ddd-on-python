from typing import Generic, Optional, Tuple, TypeVar

from kink import inject
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.planner.shared.application.mappers import dict_to_entity
from src.planner.shared.domain.value_objects.uuid import UuidValueObject
from src.planner.shared.domain.aggregates import Aggregate
from .models import Base

ModelType = TypeVar("ModelType", bound=Base)


@inject
class SqlAlcheamyRepository(Generic[ModelType]):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    For more information on how to create new methods, see:
        https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
    """

    model_class: ModelType
    entity_class: Aggregate

    def __init__(self, sqlalchemy_session: AsyncSession):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `sqlalchemy_session`: A SQLAlchemy database session object.
        """
        self.session = sqlalchemy_session


class SqlAlcheamyCreateMixin:
    async def create(self, entity: Aggregate) -> None:
        entity_object = self.model_class.from_entity(entity)  # type: ignore[attr-defined]
        self.session.add(entity_object)  # type: ignore[attr-defined]
        await self.session.commit()  # type: ignore[attr-defined]
        return None


class SqlAlcheamyFindMixin:
    async def search(self, id: UuidValueObject) -> Optional[Aggregate]:
        """Search object by id"""
        stmt = select(self.model_class).where(self.model_class.id == id.value).limit(1)  # type: ignore[attr-defined]
        return await self._search(stmt)

    async def _search(self, stmt: Select) -> Optional[Aggregate]:
        """Search object by select statement"""
        result = await self.session.execute(stmt)  # type: ignore[attr-defined]
        data = result.scalars().first()
        if data:
            return dict_to_entity(data.to_dict(), self.entity_class)  # type: ignore[attr-defined]
        return None


class SqlAlcheamyGetAllMixin:
    async def all(self, skip: int = 0, limit: int = 10) -> Tuple[Aggregate]:
        # TODO: Create SkipValueObject and LimitValueObject
        stmt = select(self.model).offset(skip)  # type: ignore[attr-defined]
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)  # type: ignore[attr-defined]
        return tuple(
            dict_to_entity(data.to_dict(), self.entity_class)  # type: ignore[attr-defined]
            for data in result.scalars().all()
        )

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
