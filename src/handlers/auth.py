from aiogram import Router
from aiogram.enums import ChatType
from aiogram.types import Message
from sqlalchemy.orm import Session

from config import CONFIG
from database import queries
from filters import filters

router: Router = Router()


@router.message(
    filters.registration_command,
    filters.TokenFilter(CONFIG.admin_token),
    lambda message: message.chat.type == ChatType.PRIVATE,
)
async def registration(
    message: Message,
    session: Session,
):
    await message.reply(
        text="Теперь ты администратор!\n\nЧем больше сила, тем больше ответственность \n © Дядя бен"
    )
    user_query = queries.public.UsersQuery(session=session)
    user_query.update(telegram_id=message.from_user.id, active=True)
