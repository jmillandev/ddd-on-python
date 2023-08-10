from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model = Base  # type: Type[ModelType]

    def __init__(self, session: async_sessionmaker[AsyncSession]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `session`: A SQLAlchemy database session object.
        """
        self.session = session

    async def create(self, object: ModelType) -> ModelType:
        # async with self.session.begin():
        self.session.add(object) 
        await self.session.commit()
        await self.session.refresh(object)
        return object
    
    async def all(self, skip: int = 0, limit: int = 10) -> List[ModelType]:
        stmt = select(self.model).offset(skip)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # TODO: Migrate method to async https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html

    # def find(self, id: Any) -> Optional[ModelType]:
    #     return self.db.query(self.model).filter(self.model.id == id).first()

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
