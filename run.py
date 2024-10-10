from bot.create_bot import create_bot, setup_dispather


async def main():
    bot = await create_bot()
    dp = await setup_dispather()
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
