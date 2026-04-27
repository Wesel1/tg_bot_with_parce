import os
from dotenv import load_dotenv

import asyncio

from openai import AsyncOpenAI

from database.database import HelpBase


ANTE_S = ('Я хочу получить чистый литературный текст — заменяй слова и обороты на более подходящие,'
          ' если нужно. Следи за корректностью описания химических и физических процессов: '
          'они должны быть правдоподобными, даже если действие происходит в вымышленном мире. '
          'В ответе предоставь только исправленный текст главы — без каких‑либо подтверждений, '
          'пояснений или комментариев к правкам. Единственное исключение — в конце можешь добавить '
          'краткие пояснения к описанным в главе физическим или химическим явлениям (если они есть).'
          'Ответ стелизуй в формате .md\n')

database = HelpBase('help.db')
load_dotenv()

async def read_from_file():
    return database.find("parce_done")

async def write_answer(answer: str) -> None:
    database.save("ai_done", answer)


async def ai_ask(count: int = 3):
    text = await read_from_file()
    try:
        client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get('API_OpenRouter'),
        )

        completion = await client.chat.completions.create(
            model="inclusionai/ling-2.6-flash:free",
            messages=[
                {"role": "user", "content": f"{ANTE_S}: {text[1]}"}
            ],
        )

        await write_answer(completion.choices[0].message.content)
    except:
        print("Ну не повезло")
        if count > 0:
            await asyncio.sleep(5)
            await ai_ask(count - 1)

if __name__ == "__main__":
    # asyncio.run(ai_ask(1))
    print(database.find("ai_done"))