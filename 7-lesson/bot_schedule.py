from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import logging, asyncio
from config import token
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher()

class Student(StatesGroup):
    name = State()
    age = State()
    phone = State()
    lesson = State()
    task = State()
    deadline = State()

student_data = {} #создаем для хронение данных о пользолвателях

@dp.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    student_data['chat_id'] = message.chat.id
    await message.answer("Привет, я бот для учета ваших заданий. Напишите ваше имя")
    await state.set_state(Student.name)

@dp.message(Student.name)
async def name(message: types.Message, state: FSMContext):
    student_data['name'] = message.text
    await message.reply("Введите ваш номер телефона")
    await state.set_state(Student.phone)

@dp.message(Student.phone)
async def phone(message: types.Message, state: FSMContext):
    student_data['phone'] = message.text
    await message.reply("Введите ваш возраст")
    await state.set_state(Student.age)

@dp.message(Student.age)
async def age(message: types.Message, state: FSMContext):
    student_data['age'] = message.text
    await message.answer("Введите свой класс")
    await state.set_state(Student.lesson)

@dp.message(Student.lesson)
async def lesson(message: types.Message, state: FSMContext):
    student_data['lesson'] = message.text
    await message.answer("Напишите свое задание")
    await state.set_state(Student.task)

@dp.message(Student.task)
async def task(message: types.Message, state: FSMContext):
    student_data['task'] = message.text
    await message.answer("Когда нужно выполнить задание (в формате дд.мм.гг чч.мм)")
    await state.set_state(Student.deadline)

@dp.message(Student.deadline)
async def deadline(message: types.Message, state: FSMContext):
    try:
        deadline_time = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
        student_data['deadline'] = deadline_time
        await message.answer(f"Задание будет выполнено в {deadline_time.strftime('%d.%m.%Y %H:%M')}")
        await schedule_task(deadline_time)
        await state.clear()
    except ValueError:
        await message.reply("Неверный формат даты, пожалуйста, используйте формат 'дд.мм.гг чч.мм'.")

async def schedule_task(deadline_time):
    now = datetime.now()
    delta = (deadline_time - now).total_seconds()

    if delta < 0:
        await bot.send_message(student_data['chat_id'], 'Это задание уже должно быть выполнено')
    else:
        await asyncio.sleep(delta)
        await task_to_perform()

async def task_to_perform():
    try:
        chat_id = student_data['chat_id']
        logging.debug(f"Айди: {chat_id}")
        await bot.send_message(chat_id, f"Задание для {student_data['name']} выполнено")
    except TelegramBadRequest as e:
        logging.error(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
