from typing import ClassVar, Dict, Protocol, runtime_checkable


@runtime_checkable
class RootAggregate(Protocol):
    __dataclass_fields__: ClassVar[Dict]
