from pydantic import BaseModel, EmailStr
from midnite.models.enumerators.transaction_types import TransactionTypes


class Users(BaseModel):
    user_id: int
    name: str
    email: EmailStr


class Transactions(BaseModel):
    transaction_id: str
    transaction_type: TransactionTypes
    transaction_amount: float
    second_received: int
    user_id: int
