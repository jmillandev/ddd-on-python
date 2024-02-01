from typing import Protocol, runtime_checkable

from .entity import Expense


@runtime_checkable
class ExpenseRepository(Protocol):

    # TODO: Use save in other repositories
    async def save(self, expense: Expense) -> None:
        ...
