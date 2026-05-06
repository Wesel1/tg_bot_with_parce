from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Начать')]
    ],
    resize_keyboard=True
)