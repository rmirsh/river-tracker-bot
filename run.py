from bot.create_bot import setup_bot, setup_dispather


async def main():
    try:
        bot = await setup_bot()
        dp = await setup_dispather()
        await dp.start_polling(bot)
    except Exception as e:
        print(f"An error occured: {e}!")

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
