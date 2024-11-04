from typing import Sequence

from sqlalchemy import select

from database.models import public
from database.queries.base import BaseQuery


class ChannelsQuery(BaseQuery):

    @staticmethod
    def _build_query(
        telegram_id: int | None,
        active: bool = False,
    ):
        stmt = select(public.Channels)
        if telegram_id:
            stmt = stmt.where(public.Channels.telegram_id == telegram_id)
        if active:
            stmt = stmt.where(public.Channels.active.is_(active))
        return stmt

    def show_channels(
        self,
        telegram_id: int | None = None,
        active: bool = False,
    ) -> Sequence[public.Channels]:
        query = self._build_query(
            telegram_id=telegram_id,
            active=active,
        )
        result = self._session.scalars(query)
        return result.all()

    def create(
        self,
        telegram_id: int,
        name: str | None = None,
    ) -> public.Channels:
        channel = public.Channels.factory(
            telegram_id=telegram_id,
            name=name,
        )
        self._session.add(channel)
        return channel

    def get_or_create(
        self,
        telegram_id: int,
        name: str | None = None,
    ):
        channels = self.show_channels(telegram_id=telegram_id)
        if len(channels) > 0:
            return channels[0]
        channel = self.create(
            telegram_id=telegram_id,
            name=name,
        )
        return channel


class UsersQuery(BaseQuery):

    @staticmethod
    def _build_query(
        telegram_id: int | None = None,
        user_id: int | None = None,
        active: bool = False,
    ):
        stmt = select(public.Users)
        if user_id:
            stmt = stmt.where(public.Users.id == user_id)
        if telegram_id:
            stmt = stmt.where(public.Users.telegram_id == telegram_id)
        if active:
            stmt = stmt.where(public.Users.active.is_(active))
        return stmt

    def show_users(
        self,
        user_id: int | None = None,
        telegram_id: int | None = None,
    ) -> Sequence[public.Users]:
        query = self._build_query(
            telegram_id=telegram_id,
            user_id=user_id,
        )
        result = self._session.scalars(query)
        return result.all()

    def create(
        self,
        telegram_id: int,
        name: str | None = None,
    ) -> public.Users:
        channel = public.Users.factory(
            telegram_id=telegram_id,
            name=name,
        )
        self._session.add(channel)
        return channel

    def get_or_create(
        self,
        telegram_id: int,
        name: str | None = None,
    ):
        channels = self.show_users(telegram_id=telegram_id)
        if len(channels) > 0:
            return channels[0]
        channel = self.create(
            telegram_id=telegram_id,
            name=name,
        )
        return channel

    def update(
        self,
        telegram_id: int,
        active: bool,
    ):
        for user in self.show_users(telegram_id=telegram_id):
            user.active = active
