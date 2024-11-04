from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from core.interfaces import Options
from filters import callback


def main_kb(
    launch_id: int | None = None,
    start_server: bool = False,
    active_user: bool = False,
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="🎮 Как начать играть?",
                callback_data=callback.HowPlay().pack(),
            ),
        ]
    ]
    if launch_id and active_user:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text="⭕️ Выключить сервер",
                    callback_data=callback.StopServer(
                        launch_id=launch_id
                    ).pack(),
                )
            ]
        )
    if start_server:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text="🟢 Запустить сервер",
                    callback_data=callback.PreparingStart().pack(),
                )
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                text="📑 Логи",
                callback_data=callback.LogsServer().pack(),
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def back_to_main() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data=callback.MainMenu().pack(),
                ),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def show_region(options: Options) -> InlineKeyboardMarkup:
    inline_keyboard = []
    row = []

    for region_id, region_name in options.options.items():
        button = InlineKeyboardButton(
            text=region_name,
            callback_data=callback.SelectRegion(region_id=region_id).pack(),
        )
        row.append(button)

        if len(row) == 2:
            inline_keyboard.append(row)
            row = []

    if row:
        inline_keyboard.append(row)

    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def show_versions(
    region_id: str,
    options: Options,
) -> InlineKeyboardMarkup:
    inline_keyboard = []
    row = []

    for version_id, version_name in options.options.items():
        button = InlineKeyboardButton(
            text=version_name,
            callback_data=callback.SelectVersion(
                region_id=region_id,
                version_id=version_id,
            ).pack(),
        )
        row.append(button)

        if len(row) == 2:
            inline_keyboard.append(row)
            row = []

    if row:
        inline_keyboard.append(row)

    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def show_slots(
    region_id: str,
    version_id: str,
    options: Options,
) -> InlineKeyboardMarkup:
    inline_keyboard = []
    row = []

    for slot_id, slot_name in options.options.items():
        button = InlineKeyboardButton(
            text=slot_name,
            callback_data=callback.SelectSave(
                region_id=region_id,
                version_id=version_id,
                slot_id=slot_id,
            ).pack(),
        )
        row.append(button)

        if len(row) == 2:
            inline_keyboard.append(row)
            row = []

    if row:
        inline_keyboard.append(row)

    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def complete_start(
    region_id: str,
    version_id: str,
    slot_id: str,
) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Нажать на рычаг...",
                    callback_data=callback.StartServer(
                        region_id=region_id,
                        version_id=version_id,
                        slot_id=slot_id,
                    ).pack(),
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
