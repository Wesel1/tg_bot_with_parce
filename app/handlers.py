from aiogram import Router, F

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message
from aiogram.fsm.state import State, StatesGroup

from pydantic import BaseModel
from typing import Optional

import app.keyboard as kb

from parcer_chance_1 import main_data_proc_par
from AI_chance_1 import ai_ask
from assistant_func import proc_link
from database.database import MyBase

router = Router()
db = MyBase('data.sql')
db.create_tables()


class ExistsNovel(StatesGroup):
    title = State()
    volume = State()
    chapter = State()

class ExistsBook(BaseModel):
    title: str
    volume: int
    chapter: int
    text: str = None

class NewNovel(StatesGroup):
    title = State()
    url = State()
    rule = State()
    volume = State()
    chapter = State()

class NewBook(BaseModel):
    id_book: int = None
    title: str
    url: str
    rule: Optional[int] = None
    volume: int
    chapter: int
    text: str = None

@router.message(Command('start'))
async def start(message: Message):
    await message.answer("Привет! 🚀", reply_markup=kb.start)

@router.message(F.text.lower() == 'начать')
async def dialogue_start(message: Message, state: FSMContext):
    await state.set_state(NewNovel.title)
    await message.answer('Введите название произведения')

@router.message(NewNovel.title)
async def process_volume(message: Message, state: FSMContext):
    if db.get_book(title=message.text.lower()):
        await state.set_state(ExistsNovel.volume)
        await state.update_data(title=message.text.lower())
        await message.answer('Эта книгу уже кто-то искал, осталось только выбрать главу\nТеперь напиши номер тома')
    else:
        await state.update_data(title=message.text.lower())
        await state.set_state(NewNovel.url)
        await message.answer('Отправь ссылку на книгу с любой страницы(сайт RanobeLib)')

@router.message(NewNovel.url)
async def get_url(message: Message, state: FSMContext):
    await state.update_data(url=proc_link(message.text))
    await state.set_state(NewNovel.volume)
    await message.answer('Введи том')

@router.message(ExistsNovel.volume)
async def get_chapter(message: Message, state: FSMContext):
    await state.update_data(volume=int(message.text))
    await state.set_state(ExistsNovel.chapter)
    await message.answer("Введи главу")

@router.message(NewNovel.volume)
async def get_chapter(message: Message, state: FSMContext):
    await state.update_data(volume=int(message.text))
    await state.set_state(NewNovel.chapter)
    await message.answer("Введи главу")

@router.message(ExistsNovel.chapter)
async def get_exists_chapter(message: Message, state: FSMContext):
    await state.update_data(chapter=int(message.text))
    data = await state.get_data()
    data_for_db = ExistsBook.model_validate(data)

    book_id = db.get_book(title=data_for_db.title)
    data_for_db.text = db.get_chapters_by_book_id(book_id=book_id, volume=data_for_db.volume, chapter=data_for_db.chapter)

    document = BufferedInputFile(data_for_db.text.encode('utf-8'), filename=f"Глава_{data_for_db.chapter}.md")
    await message.answer_document(document, caption=f'Вот глава {data_for_db.chapter}')
    db.conn_close()
    await state.clear()


@router.message(NewNovel.chapter)
async def get_chapter(message: Message, state: FSMContext):
    await state.update_data(chapter=int(message.text))
    data = await state.get_data()
    data_for_db = NewBook.model_validate(data)


    text = await main_data_proc_par(data_for_db.url, data_for_db.volume, data_for_db.chapter)
    data_for_db.text = await ai_ask(text)


    data_for_db.id_book = db.add_book(title = data_for_db.title.lower(), url=data_for_db.url)
    db.add_chapter(book_id=data_for_db.id_book, volume= data_for_db.volume, chapter= data_for_db.chapter, text=data_for_db.text)


    document = BufferedInputFile(data_for_db.text.encode('utf-8'), filename=f"Глава_{data_for_db.chapter}.md")
    await message.answer_document(document, caption=f'Вот глава {data_for_db.chapter}')
    db.conn_close()
    await state.clear()


# @router.message(NovelStates.volume)
# async def process_chapter(message: Message, state: FSMContext):
#     await state.update_data(chapter=int(message.text))
#
#     data = await state.get_data()
#
#     await message.answer('Пока что все шикарно')
#
#
#
#     document = BufferedInputFile(doc.encode('utf-8'), filename=f"Глава_{data['chapter']}.md")
#     await message.answer_document(document, caption=f'Вот глава {data['chapter']}')
#
#     await state.clear()