from pydantic import BaseModel
from typing import List
from datetime import date


class Transaction(BaseModel):

    transaction_date: date

    description: str

    transaction_type: str

    amount: float

    currency: str = "USD"


class CustomerEntities(BaseModel):

    customer_name: str

    customer_id: str


class AccountEntities(BaseModel):

    account_number: str

    swift_code: str = ""


class BalanceEntities(BaseModel):

    opening_balance: float

    closing_balance: float

    currency: str = "USD"


class BankStatementEntities(BaseModel):

    customer_entities: CustomerEntities

    account_entities: AccountEntities

    balance_entities: BalanceEntities

    transaction_entities: List[Transaction]