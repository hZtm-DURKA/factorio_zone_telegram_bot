from collections.abc import Callable, Awaitable
from typing import Any

from aiogram.types import Update

from core.connection import DATABASE


async def db_connection_mw(
    handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
    event: Update,
    data: dict[str, Any],
) -> Any:
    with DATABASE.session() as session:
        data["session"] = session
        result = await handler(event, data)
        session.flush()
        session.commit()
        return result
