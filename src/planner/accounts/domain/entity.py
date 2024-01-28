from src.planner.accounts.domain.events import AccountCreated
from src.planner.accounts.domain.value_objects import (
    AccountBalance,
    AccountCurrency,
    AccountId,
    AccountName,
)
from src.planner.shared.domain.aggregates import AggregateRoot
from src.planner.shared.domain.users import UserId


class Account(AggregateRoot):
    id: AccountId
    user_id: UserId
    name: AccountName
    currency: AccountCurrency
    balance: AccountBalance

    def __str__(self) -> str:
        return f"[{self.id}] {self.name}"

    @classmethod
    def create(cls, 
            id: AccountId,
            user_id: UserId,
            name: AccountName,
            currency: AccountCurrency,
            balance: AccountBalance):
        account = cls(id=id, user_id=user_id, name=name, currency=currency, balance=balance)
        account._record_event(
            AccountCreated.make(
                account.id.value,
                user_id=account.user_id.value,
                name=account.name.primitive,
                currency=account.currency.primitive,
                balance=account.balance.primitive,
            )
        )
        return account