import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

import middlewares
from commands import commands
from config import CONFIG
from core.connection import DATABASE
from handlers import start, how_to_play, server, auth
from misc.factorio_zone import WebSocketFactorioZone, FactorioZone

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    await bot.set_my_commands([])


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    bot: Bot = Bot(
        token=CONFIG.telegram.token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp: Dispatcher = Dispatcher()

    dp.include_router(auth.router)
    dp.include_router(start.router)
    dp.include_router(how_to_play.router)
    dp.include_router(server.router)

    await commands.set_commands(bot=bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup(bot)
    factorio_zone = FactorioZone(
        token=CONFIG.factorio_zone.token,
        factorio_ws=WebSocketFactorioZone(bot=bot),
    )
    await factorio_zone.connect()
    middlewares.setup(dispatcher=dp)
    DATABASE.engine.connect()
    await dp.start_polling(bot, factorio_zone=factorio_zone)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
