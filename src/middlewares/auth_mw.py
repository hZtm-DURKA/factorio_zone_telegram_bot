from collections.abc import Awaitable
from typing import Callable, Any

from aiogram import types
from aiogram.types import Update
from loguru import logger
from sqlalchemy.orm import Session

from database import queries


async def auth_middleware(
    handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
    event: Update,
    data: dict[str, Any],
) -> Any:
    session: Session = data.get("session")
    if not session:
        raise Exception("session not initialized!")
    channel_query = queries.public.ChannelsQuery(session=session)
    users_query = queries.public.UsersQuery(session=session)

    user = users_query.get_or_create(
        telegram_id=event.event.from_user.id,
        name=event.event.from_user.full_name,
    )
    channel = channel_query.get_or_create(
        telegram_id=(
            event.event.chat.id
            if isinstance(event.event, types.Message)
            else event.event.chat_instance
        ),
        name=(
            event.event.chat.full_name
            if isinstance(event.event, types.Message)
            else None
        ),
    )
    data["user"] = user
    data["channel"] = channel
    if not user.active:
        logger.info(f"User {user.telegram_id=} not active")
    return await handler(event, data)
