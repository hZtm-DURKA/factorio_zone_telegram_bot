from aiogram import types, Bot
from attr import dataclass
from loguru import logger

from core.connection import DATABASE
from core.interfaces import StatusEnum, StatusWS
from database import queries
from keyboards import keyboards

_TEXT = """Адрес: <code>{address}</code>
Статус: {status_server}
Сокет: {status_socket}
"""
_TEXT_SLOT = """Регион: {region}
Сохранение: {slot}
Версия: {version}
"""


@dataclass
class MessageDTO:
    text: str
    keyword: types.InlineKeyboardMarkup


def get_statis_emoji(status: StatusEnum) -> str:
    if status == StatusEnum.running:
        return "🟢"
    if status == StatusEnum.stopping:
        return "⭕️"
    return "🟡"


def get_message_status(
    status: StatusWS,
    active_user: bool = False,
) -> MessageDTO:
    main_text = _TEXT.format(
        status_server=f"{get_statis_emoji(status.server.type)} {status.server.type.value.capitalize()}",
        status_socket="Active" if status.running_ws else "Connecting...",
        address=(
            status.server.socket
            if status.server.socket
            else "Address not assigned"
        ),
    )
    if status.slot:
        slot_info = _TEXT_SLOT.format(
            region=status.slot.region,
            slot=status.slot.slot,
            version=status.slot.version,
        )
        main_text = main_text + f"\n{slot_info}"
    keyboard = keyboards.main_kb(
        launch_id=(
            status.server.launchId
            if status.server.type == StatusEnum.running
            else None
        ),
        start_server=status.server.type == StatusEnum.stopping,
        active_user=active_user,
    )
    return MessageDTO(text=main_text, keyword=keyboard)


async def _edit_message(
    bot: Bot,
    message_dto: MessageDTO,
    channel_id: int,
    message_id: int,
) -> bool:
    try:
        await bot.edit_message_text(
            chat_id=channel_id,
            text=message_dto.text,
            message_id=message_id,
        )
        return True
    except Exception as ex:
        logger.warning(f"Edit message {ex=}")
        return False


async def _send_message(
    bot: Bot,
    message_dto: MessageDTO,
    channel_id: int,
) -> bool:
    try:
        await bot.send_message(
            chat_id=channel_id,
            text=message_dto.text,
        )
        return True
    except Exception as ex:
        logger.warning(f"Send message {ex=}")
        return False


async def broadcast_server_status(
    bot: Bot,
    status: StatusWS,
):
    with DATABASE.session() as session:
        channels_query = queries.public.ChannelsQuery(session=session)
        message_dto = get_message_status(status=status)
        for channel in channels_query.show_channels(active=True):
            try:
                if channel.message_id:
                    if await _edit_message(
                        bot=bot,
                        message_dto=message_dto,
                        channel_id=channel.telegram_id,
                        message_id=channel.message_id,
                    ):
                        continue
                await _send_message(
                    bot=bot,
                    message_dto=message_dto,
                    channel_id=channel.telegram_id,
                )
            except Exception as ex:
                logger.warning(f"Event change server | {channel} {ex}")
