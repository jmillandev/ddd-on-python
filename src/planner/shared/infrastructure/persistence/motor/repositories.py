from abc import ABCMeta
from dataclasses import asdict
from datetime import date, datetime, timezone
from typing import Optional

from kink import inject
from motor.core import AgnosticCollection, AgnosticDatabase


def object_to_mongo_type(value):
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc)
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day)
    return value


@inject
class MotorRepository(metaclass=ABCMeta):
    """
    Abstract class for the MotorRepository(MongoDB) class.
    """

    COLLECTION_NAME: str
    _collection: Optional[AgnosticCollection]

    def __init__(self, database: AgnosticDatabase):
        """
        **Parameters**

        * `database`: A AgnosticDatabase database object.
        """
        self.database = database
        self._collection = None

    @property
    def collection(self):
        if self._collection is None:
            self.init_collection()
        return self._collection

    def init_collection(self) -> None:
        if not self.COLLECTION_NAME:
            raise NotImplementedError(
                f"define {self.__class__.__name__}.COLLECTION_NAME or"
                " override {self.__class__.__name__}.init_collection method."
            )
        self._collection = self.database.get_collection(self.COLLECTION_NAME)

    def aggregate_to_dict(self, aggregate) -> dict:
        data = asdict(aggregate)
        for key in data:
            data[key] = object_to_mongo_type(data[key].value)
        return data
