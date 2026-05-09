import os
import asyncio
from dotenv import load_dotenv

import redis.asyncio as aioredis

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from app.handlers import router, db

async def ante_scr():
    print('Все шикарно')

async def post_scr():
    db.conn_close()

async def main() -> None:
    load_dotenv()
    redis = await aioredis.from_url('redis://localhost:6379/0')
    bot = Bot(token=os.environ.get('TOKEN_BOT'))
    dp = Dispatcher(storage=RedisStorage(redis))
    dp.include_router(router)

    await ante_scr()

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

