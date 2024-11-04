from datetime import datetime

from sqlalchemy import Integer, DateTime, func, Boolean, false
from sqlalchemy.orm import Mapped, mapped_column


class IDMixin:
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )


class ActiveMixin:
    active: Mapped[bool] = mapped_column(
        Boolean,
        server_default=false(),
        default=False,
    )


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )
