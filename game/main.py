import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import Config
from handlers import router

async def main():
    logging.basicConfig(level=logging.INFO)

    config = Config()
    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())