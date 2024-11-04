from aiogram import Router
from aiogram.enums import ChatType
from aiogram.types import Message, CallbackQuery

from database.models import public
from filters import filters, callback
from helpers.status_server import get_message_status
from misc.factorio_zone import FactorioZone

router: Router = Router()


@router.message(
    filters.start_command,
    lambda message: message.chat.type == ChatType.GROUP,
)
async def start(
    message: Message,
    factorio_zone: FactorioZone,
    user: public.Users,
    channel: public.Channels,
):
    status = await factorio_zone.status()
    message_dto = get_message_status(
        status=status,
        active_user=user.active,
    )
    message = await message.answer(
        text=message_dto.text,
        reply_markup=message_dto.keyword,
    )
    channel.message_id = message.message_id


@router.callback_query(callback.MainMenu.filter())
async def back_to_main(
    callback_query: CallbackQuery,
    factorio_zone: FactorioZone,
    user: public.Users,
):
    status = await factorio_zone.status()
    message_dto = get_message_status(
        status=status,
        active_user=user.active,
    )
    await callback_query.message.edit_text(
        text=message_dto.text,
        reply_markup=message_dto.keyword,
    )
