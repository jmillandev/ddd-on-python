from src.planner.accounts.domain.events import AccountCreated, AccountBalanceUpdated
from src.planner.accounts.domain.value_objects import (
    AccountBalance,
    AccountCurrency,
    AccountName,
    AccountDeltaBalance
)
from src.planner.shared.domain.accounts import AccountId
from src.planner.shared.domain.aggregates import AggregateRoot, aggregate_dataclass
from src.planner.shared.domain.users import UserId


@aggregate_dataclass
class Account(AggregateRoot):
    id: AccountId
    owner_id: UserId
    name: AccountName
    currency: AccountCurrency
    balance: AccountBalance

    def __str__(self) -> str:
        return f"Account(id={self.id}, owner_id={self.owner_id})"

    @classmethod
    def create(
        cls,
        id: AccountId,
        owner_id: UserId,
        name: AccountName,
        currency: AccountCurrency,
        balance: AccountBalance,
    ):
        account = cls(
            id=id, owner_id=owner_id, name=name, currency=currency, balance=balance
        )
        account._record_event(
            AccountCreated.make(
                account.id.primitive,
                owner_id=account.owner_id.primitive,
                name=account.name.primitive,
                currency=account.currency.primitive,
                balance=account.balance.primitive,
            )
        )
        return account

    def update_balance(self, delta_balance: AccountDeltaBalance) -> None:
        self.balance += delta_balance
        self._record_event(
            AccountBalanceUpdated.make(
                self.id.primitive,
                owner_id=self.owner_id.primitive,
                name=self.name.primitive,
                currency=self.currency.primitive,
                balance=self.balance.primitive,
            )
        )
