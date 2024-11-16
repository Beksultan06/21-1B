from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

keybord_main = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='ИНФО')],
            [KeyboardButton(text='Контакты')],
            [KeyboardButton(text='О нас')],
        ],
        resize_keyboard=True)

keybord_direction = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text='Бэкенд')],
        [KeyboardButton(text='Фронт')],
        [KeyboardButton(text='Дизайн')],
        [KeyboardButton(text='Назад')],
    ],
    resize_keyboard=True
)

keybord_back = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True
)