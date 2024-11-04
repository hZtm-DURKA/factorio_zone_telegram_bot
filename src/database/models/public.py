from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import Base
from . import _mixins


class Public(Base):
    __abstract__ = True


class Users(
    Public,
    _mixins.IDMixin,
    _mixins.ActiveMixin,
    _mixins.CreatedAtMixin,
):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    @classmethod
    def factory(
        cls,
        telegram_id: int,
        name: str | None = None,
    ):
        return cls(telegram_id=telegram_id, name=name)


class Channels(
    Public,
    _mixins.IDMixin,
    _mixins.ActiveMixin,
    _mixins.CreatedAtMixin,
):
    __tablename__ = "channels"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )
    message_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    @classmethod
    def factory(
        cls,
        telegram_id: int,
        name: str | None = None,
    ):
        return cls(
            telegram_id=telegram_id,
            name=name,
        )
