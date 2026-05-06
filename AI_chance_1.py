import os
from dotenv import load_dotenv

import asyncio

from openai import AsyncOpenAI

load_dotenv()

ANTE_S = ('Я хочу получить чистый литературный текст — заменяй слова и обороты на более подходящие,'
          ' если нужно. Корректно отобрази диалоги, как в книгах. Следи за корректностью описания химических и физических процессов: '
          'они должны быть правдоподобными, даже если действие происходит в вымышленном мире. '
          'В ответе предоставь только исправленный текст главы. Единственное исключение — в конце можешь добавить '
          'краткие пояснения к описанным в главе физическим или химическим явлениям (если они есть).'
          'Ответ стелизуй в формате .md')

async def ai_ask(text: str) -> str:
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get('API_OpenRouter'),
    )

    completion = await client.chat.completions.create(
        # model="inclusionai/ling-2.6-flash:free",
        model = 'nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free',
        messages=[
            {"role": "user", "content": f"{ANTE_S}:\n{text}"}
        ],
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


if __name__ == "__main__":
    asyncio.run(ai_ask('Hi'))




