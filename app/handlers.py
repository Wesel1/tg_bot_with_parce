from aiogram import Router, F

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
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


class Novel(StatesGroup):
    title = State()
    url = State()
    volume = State()
    chapter = State()

class Book(BaseModel):
    book_id: Optional[int] = None
    title: str
    url: Optional[str] = None
    volume: int
    chapter: int
    text: Optional[str] = None


async def build_chapter(
        data_for_db: Book,
        db: MyBase,
):
    if data_for_db.url:
        text = await main_data_proc_par(data_for_db.url, data_for_db.volume, data_for_db.chapter)
        data_for_db.text = await ai_ask(text)

        data_for_db.id_book = db.add_book(title=data_for_db.title.lower(), url=data_for_db.url)
        db.add_chapter(book_id=data_for_db.id_book, volume=data_for_db.volume,
                       chapter=data_for_db.chapter, text=data_for_db.text)

    else:
        data_for_db.book_id, data_for_db.url = db.get_book(title=data_for_db.title)

        text = db.get_chapters_by_book_id(book_id=data_for_db.book_id, volume=data_for_db.volume,
                                          chapter=data_for_db.chapter)
        if text:
            data_for_db.text = text['text']
        else:
            text = await main_data_proc_par(data_for_db.url, data_for_db.volume, data_for_db.chapter)
            data_for_db.text = await ai_ask(text)

            db.add_chapter(book_id=data_for_db.book_id, volume=data_for_db.volume,
                           chapter=data_for_db.chapter, text=data_for_db.text)


@router.message(Command('start'))
async def start(message: Message):
    await message.answer("Привет! 🚀", reply_markup=kb.start)

@router.message(F.text.lower() == 'начать')
async def dialogue_start(message: Message, state: FSMContext):
    await state.set_state(Novel.title)
    await message.answer('Введите название произведения', reply_markup=ReplyKeyboardRemove())

@router.message(Novel.title)
async def process_volume(message: Message, state: FSMContext):
    await state.update_data(title=message.text.lower())
    if db.get_book(title=message.text.lower()):
        await state.set_state(Novel.volume)
        await message.answer('Эта книгу уже кто-то искал, осталось только выбрать главу\nТеперь напиши номер тома')
    else:
        await state.set_state(Novel.url)
        await message.answer('Отправь ссылку на книгу с любой страницы(сайт RanobeLib)')

@router.message(Novel.url)
async def get_url(message: Message, state: FSMContext):
    await state.update_data(url=proc_link(message.text))
    await state.set_state(Novel.volume)
    await message.answer('Введи том')

@router.message(Novel.volume)
async def get_chapter(message: Message, state: FSMContext):
    await state.update_data(volume=int(message.text))
    await state.set_state(Novel.chapter)
    await message.answer("Введи главу")

@router.message(Novel.chapter)
async def get_chapter(message: Message, state: FSMContext):
    await state.update_data(chapter=int(message.text))
    data = await state.get_data()
    data_for_db = Book.model_validate(data)

    await build_chapter(data_for_db, db)

    dialogue_continue = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data=f'cont:{data_for_db.title}:{data_for_db.volume}:{data_for_db.chapter + 1}')],
        [InlineKeyboardButton(text='Нет', callback_data='stop')]
    ]
    )

    document = BufferedInputFile(data_for_db.text.encode('utf-8'), filename=f"Глава_{data_for_db.chapter}.md")
    await message.answer_document(document, caption=f'Вот глава {data_for_db.chapter}')
    await message.answer("Продолжим со следующей главы?", reply_markup=dialogue_continue)

    await state.clear()

@router.callback_query(F.data.startswith('cont:'))
async def continue_dialogue(callback: CallbackQuery):
    data_from_callback = callback.data.split(':')
    data_for_db = Book(
        title = data_from_callback[1],
        volume= data_from_callback[2],
        chapter= data_from_callback[3]
    )

    await build_chapter(data_for_db, db)
    dialogue_continue = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да',
                              callback_data=f'cont:{data_for_db.title}:{data_for_db.volume}:{data_for_db.chapter + 1}')],
        [InlineKeyboardButton(text='Нет', callback_data='stop')]
    ]
    )

    document = BufferedInputFile(data_for_db.text.encode('utf-8'), filename=f"Глава_{data_for_db.chapter}.md")
    await callback.message.answer_document(document, caption=f'Вот глава {data_for_db.chapter}', reply_markup=dialogue_continue)

@router.callback_query(F.data == 'stop')
async def stop_query(callback: CallbackQuery):
    await callback.message.answer('Приятно было работать с тобой', reply_markup=kb.start)

# @router.message(Novel.chapter)
# async def get_chapter(message: Message, state: FSMContext):
#     await state.update_data(chapter=int(message.text))
#     data = await state.get_data()
#     data_for_db = Book.model_validate(data)
#
#
#     text = await main_data_proc_par(data_for_db.url, data_for_db.volume, data_for_db.chapter)
#     data_for_db.text = await ai_ask(text)
#
#
#     data_for_db.id_book = db.add_book(title = data_for_db.title.lower(), url=data_for_db.url)
#     db.add_chapter(book_id=data_for_db.id_book, volume= data_for_db.volume,
#                    chapter= data_for_db.chapter, text=data_for_db.text)
#
#
#     document = BufferedInputFile(data_for_db.text.encode('utf-8'),
#                                  filename=f"Глава_{data_for_db.chapter}.md")
#     await message.answer_document(document, caption=f'Вот глава {data_for_db.chapter}')
#     await message.answer('Хотите обработать следующую главу?',
#                          reply_markup=kb.dialogue_continue)

