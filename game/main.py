# импорт модуля асинхронного программирования
import asyncio
# импорт модуля для логирования (записи событий)
import logging
# импорт классов бота и диспетчера из aiogram
from aiogram import Bot, Dispatcher

# импорт класса конфигурации из файла config.py
from config import Config
# импорт роутера из файла handlers.py
from handlers import router

# асинхронная основная функция
async def main():
    # настройка базового логирования с уровнем INFO (информационные сообщения)
    logging.basicConfig(level=logging.INFO)

    # создание экземпляра конфигурации
    config = Config()
    # создание экземпляра бота с токеном из конфигурации
    bot = Bot(token=config.bot_token)
    # создание экземпляра диспетчера для обработки сообщений
    dp = Dispatcher()

    # подключение роутера к диспетчеру
    dp.include_router(router)

    # удаление вебхука (если был установлен) и пропуск ожидающих обновлений
    await bot.delete_webhook(drop_pending_updates=True)
    # запуск опроса серверов telegram для получения обновлений
    await dp.start_polling(bot)

# проверка, что скрипт запущен напрямую, а не импортирован
if __name__ == '__main__':
    # запуск асинхронной функции main с помощью asyncio.run
    asyncio.run(main())