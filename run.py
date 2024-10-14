import logging
import asyncio
from aiogram import Bot, Dispatcher
from bot.create_bot import setup_bot, setup_dispather  # Ваши функции для настройки бота
from config import settings  # Ваши настройки


# Настройка логгера
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ]
    )
    logging.getLogger("aiogram").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.INFO)


async def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        logger.info("Запуск бота...")

        bot = await setup_bot(
            delete_webhooks=True if not settings.general.is_prod else False,
        )
        dp = await setup_dispather()

        logger.info("Бот успешно настроен, запускаем polling")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
