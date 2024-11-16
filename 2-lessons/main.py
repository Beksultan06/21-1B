from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio, logging
from config import token

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher()

MENU = {
    'Эспрессо': 150,
    'Капучино': 150,
    'Латте': 130,
    'Американо': 200,
    '3 в 1': 50,
}

orders = {}

@dp.message(Command("start"))
async def start(message:types.Message):
    await message.answer("Добро пожаловать в кофейню☕! \n Выберите из меню: /menu")

@dp.message(Command("menu"))
async def menu_command(message:types.Message):
    builder = InlineKeyboardBuilder()

    for coffe, price in MENU.items():
        builder.button(
            text=f"{coffe} - {price}",
            callback_data=f'menu_{coffe}'
        )
    builder.adjust(1)
    await message.answer("Меню напитков: ", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("menu_"))
async def choose_coffe(callback: types.CallbackQuery):
    coffee = callback.data.split("_")[1]
    orders[callback.from_user.id] = {"coffee": coffee, "quantity": 1}

    builder = InlineKeyboardBuilder()
    for i in range(1, 6):
        builder.button(
            text=str(i),
            callback_data=f"quantity_{i}"
        )
    builder.adjust(2)
    await callback.message.answer(f"Вы выбрали {coffee}. Укажите количество: ", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("quantity_"))
async def choose_quantity(callback: types.CallbackQuery):
    quantity = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    if user_id in orders:
        orders[user_id]['quantity'] = quantity
        coffee = orders[user_id]['coffee']
        price = MENU[coffee] * quantity

        builder = InlineKeyboardBuilder()
        builder.button(
            text = 'Подтверить заказ',
            callback_data='confirm_orders'
        )

        await callback.message.answer(
            f"Ваш заказ: {coffee} x{quantity} = {price}сомов.\nПодтвердите заказ?",
            reply_markup=builder.as_markup()
        )

@dp.callback_query(F.data == 'confirm_orders')
async def confirm_orders(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id in orders:
        coffee = orders[user_id]['coffee']
        quantity = orders[user_id]['quantity']
        total_price = MENU[coffee] * quantity

        del orders[user_id]

        await callback.message.answer(
            f"спасибо за заказ!\nВы заказали: {coffee} x{quantity}.\nИтого к оплате: {total_price}сомов."
        )

@dp.message(Command("info"))
async def info(message: types.Message):
    await message.answer("Информация о кофейне☕!!!")

async def main():
    await dp.start_polling(bot)

if __name__=='__main__':
    asyncio.run(main())