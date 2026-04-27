import os
import asyncio
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
# from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router
from database.database import HelpBase

async def ante_scr():
    print('Все шикарно')



async def main() -> None:
    load_dotenv()
    bot = Bot(token=os.environ.get('TOKEN_BOT'))
    # storage = MemoryStorage()
    dp = Dispatcher()
    dp.include_router(router)
    await ante_scr()

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

