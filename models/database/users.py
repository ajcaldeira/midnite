from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from midnite.models.database.base import MidniteBase
from midnite.models.enumerators.transaction_types import TransactionTypes
import uuid


class Users(MidniteBase):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()

    ## One-to-many: One user has many transactions
    transactions: Mapped[list["Transactions"]] = relationship()


class Transactions(MidniteBase):
    __tablename__ = "transactions"

    ## One-to-many: One user has many transactions
    transaction_id: Mapped[str] = mapped_column(
        primary_key=True, unique=True, default=uuid.uuid4, index=True
    )
    transaction_type: Mapped[TransactionTypes] = mapped_column()
    transaction_amount: Mapped[float] = mapped_column()
    second_received: Mapped[int] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
