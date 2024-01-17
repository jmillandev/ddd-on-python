from dataclasses import dataclass
from typing import Optional



@dataclass(frozen=True)
class FindAuthTokenQuery:
    access_token: Optional[str]
