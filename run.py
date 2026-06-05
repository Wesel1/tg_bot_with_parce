import os
import asyncio
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

from app.handlers import router
from database.session import engine
from database.session import create_db


async def ante_scr():
    print("Все шикарно")
    await create_db()


async def post_scr():
    await engine.dispose()


async def main() -> None:
    load_dotenv()

    bot = Bot(token=os.environ.get("TOKEN_BOT"))
    dp = Dispatcher()
    dp.include_router(router)

    await ante_scr()
    await dp.start_polling(bot)
    await post_scr()
    print("Закрыли engine")


if __name__ == "__main__":
    asyncio.run(main())
