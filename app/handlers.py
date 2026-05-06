from aiogram import Router, types, F

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.fsm.state import State, StatesGroup

import app.keyboard as kb

from parcer_chance_1 import main_data_proc_par
from AI_chance_1 import ai_ask
from database.database import MyBase

router = Router()

class NewNovelStates(StatesGroup):
    title: str
    url: str


class NovelStates(StatesGroup):
    volume = State()
    chapter = State()

@router.message(Command('start'))
async def start(message: types.Message):
    await message.answer("Привет! 🚀", reply_markup=kb.start)

@router.message(F.text.lower() == 'Начать')
async def dialogue_start(message: types.Message, state: FSMContext):
    await state.set_state(NovelStates.volume)
    await message.answer('Напишите номер тома')

@router.message(NovelStates.volume)
async def process_volume(message: types.Message, state: FSMContext):
    await state.update_data(volume=int(message.text))
    await state.set_state(NovelStates.chapter)
    await message.answer('Теперь напиши номер страницы')

@router.message(NovelStates.chapter)
async def process_chapter(message: types.Message, state: FSMContext):
    await state.update_data(chapter=int(message.text))

    data = await state.get_data()

    await message.answer('Пока что все шикарно')

    text = await main_data_proc_par(data['volume'], data['chapter'])
    doc = await ai_ask(text)

    document = BufferedInputFile(doc.encode('utf-8'), filename=f"Глава_{data['chapter']}.md")
    await message.answer_document(document, caption=f'Вот глава {data['chapter']}')

    await state.clear()