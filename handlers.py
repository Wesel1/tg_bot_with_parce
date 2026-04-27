from aiogram import Router, types, F

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.fsm.state import State, StatesGroup

from parcer_chance_1 import main_data_proc_par
from AI_chance_1 import ai_ask
from database.database import HelpBase

router = Router()
db = HelpBase('help.db')

class NovelStates(StatesGroup):
    volume = State()
    chapter = State()

@router.message(Command('start'))
async def start(message: types.Message):
    await message.answer("Привет! 🚀")

@router.message(F.text.lower() == 'погнали')
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

    await main_data_proc_par(data['volume'], data['chapter'])
    await ai_ask()

    document = BufferedInputFile(db.find('ai_done')[1].encode('utf-8'), filename="report.md")
    await message.answer_document(document, caption='Вот ваша глава')

    await state.clear()