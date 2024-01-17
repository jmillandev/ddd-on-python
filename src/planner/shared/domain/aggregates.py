from typing import Protocol, runtime_checkable, ClassVar, Dict


@runtime_checkable
class Aggregate(Protocol):
    __dataclass_fields__: ClassVar[Dict] 
