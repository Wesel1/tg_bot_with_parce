import os
import asyncio
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

from app.handlers import router
from database.db_instance import db


async def ante_scr():
    print("Все шикарно")
    await db.setup()
    await db.create_tables()


async def post_scr():
    await db.close()


async def main() -> None:
    load_dotenv()

    bot = Bot(token=os.environ.get("TOKEN_BOT"))
    dp = Dispatcher()
    dp.include_router(router)

    await ante_scr()

    await dp.start_polling(bot)
    print("Закрыли бд")
    await post_scr()


if __name__ == "__main__":
    asyncio.run(main())
