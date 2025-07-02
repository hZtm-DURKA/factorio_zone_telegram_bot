from aiogram import Bot
from aiogram.types import BotCommand

ListCommands: list[BotCommand] = [
    BotCommand(
        command="/factorio",
        description="Factorio server (factorio.zone)",
    )
]


async def set_commands(bot: Bot):
    await bot.set_my_commands(commands=ListCommands)
