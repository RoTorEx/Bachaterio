import asyncio
from typing import Union

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs

from src.bot.dialogs.base import load_dialogs
from src.bot.handlers.base import load_handlers
from src.infrastructure.config_reader import settings
from src.infrastructure.database import redis_connection
from src.infrastructure.logger_builder import build_logger


async def main() -> None:
    """Application entrypoint"""

    storage: Union[RedisStorage, MemoryStorage]

    # ?Choosing Memory Storage
    if settings.tg_bot.use_redis:
        storage = redis_connection(settings.redis)

    else:
        storage = MemoryStorage()

    # ?Creating bot and its dispatcher
    bot = Bot(token=settings.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    # ?Register all components and setup dialogs. Dialog loader must goes last!
    dp.include_router(load_handlers())
    dp.include_router(load_dialogs())
    setup_dialogs(dp)

    try:
        await dp.start_polling(bot)

    finally:
        await dp.fsm.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    logger = build_logger(__name__)

    try:
        logger.warning("Starting bot...")
        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        logger.warning("All pools and session closed. Bot stopped successfully!")
