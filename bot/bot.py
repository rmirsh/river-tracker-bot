from dotenv import load_dotenv
import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(f"Hello {hbold(message.from_user.first_name)}!")


async def main():
    bot = Bot('6744838238:AAHXxj5NFPBsBw9msk_N86dkJ0jN5-qz0hI', parse_mode=ParseMode.HTML)
    await dp.start_polling(bot) 


if __name__=="__main__":
    asyncio.run(main())
