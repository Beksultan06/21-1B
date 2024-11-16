from config import token
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
import logging, asyncio
from button import keybord_direction, keybord_back, keybord_main

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message:types.Message):
    # await message.reply("Привет! Добро пожаловать!!!")
    await message.answer("Привет! Добро пожаловать!!!", reply_markup=keybord_main)

@dp.message(lambda message: message.text == 'Контакты')
async def contact(message: types.Message):
    keybord = types.ReplyKeyboardMarkup(
        keyboard = [
            [types.KeyboardButton(text='Бекзат')],
            [types.KeyboardButton(text='Али')],
            [types.KeyboardButton(text='Саидахмад')],
            [types.KeyboardButton(text='Яхё')],
            [types.KeyboardButton(text='Баха')],
            [types.KeyboardButton(text='Назад')]
        ],
        resize_keyboard=True
    )
    await message.answer("Информация о группе 21-1B", reply_markup=keybord)

@dp.message(lambda message: message.text in ['Бекзат', 'Али', 'Саидахмад', 'Яхё', 'Баха'])
async def info_students(message: types.Message):
    if message.text == 'Бекзат':
        await message.answer("Информация о Бекзат")
    elif message.text == 'Али':
        await message.answer("Информация о Али")
    elif message.text == 'Саидахмад':
        await message.answer("Информация о Саидахмад")
    elif message.text == 'Яхё':
        await message.answer("Информация о Яхё")
    elif message.text == 'Баха':
        await message.answer("Информация о Баха")
    else:
        await message.answer("Бексултан")

@dp.message(F.text=='ИНФО')
async def info_direction(message: types.Message):
    await message.answer("Информация о направлениях", reply_markup=keybord_direction)

@dp.message(lambda message: message.text in ['Бэкенд', 'Фронт', 'Дизайн'])
async def info(message: types.Message):
    if message.text == 'Бэкенд':
        await message.answer("Информация о Бэкенд")
    elif message.text == 'Фронт':
        await message.answer("Информация о Фронт")
    elif message.text == 'Дизайн':
        await message.answer("Информация о Дизайн")
    logging.info("Кнопки рабочие")

@dp.message(F.text=='О нас')
async def about(message: types.Message):
    await message.reply("Инфо о нас", reply_markup=keybord_back)

@dp.message(F.text=='Назад')
async def back(message: types.Message):
    await message.answer("Идем назад", reply_markup=keybord_main)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())