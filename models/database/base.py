from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class MidniteBase(DeclarativeBase):
    """
    Base model for all models in the application.

    """

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        unique=False, nullable=False, default=datetime.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        unique=False, nullable=False, default=datetime.now()
    )
