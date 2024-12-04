from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import logging, asyncio
from config import token
import aioschedule as schedule
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher()

# Создаем класс состояний
class Form(StatesGroup):
    name = State()  # Состояние для имени
    phone = State()  # Состояние для телефона
    age = State()  # Состояние для возраста
    class_name = State()  # Состояние для класса
    lesson = State()  # Состояние для урока
    task = State()  # Состояние для задания
    deadline = State()  # Состояние для дедлайна

# Словарь для хранения данных студента
student_data = {}

# Обработчик для команды /start
@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer("Привет! Я бот для учета ваших заданий. Напишите ваше имя.")
    await Form.name.set()  # Устанавливаем состояние для имени

# Обработчик для состояния name
@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    student_data['name'] = message.text
    await message.reply("Введите ваш номер телефона")
    await state.set_state(Form.phone)  # Переходим к следующему состоянию

# Обработчик для состояния phone
@dp.message(Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    student_data['phone'] = message.text
    await message.reply("Введите ваш возраст")
    await state.set_state(Form.age)  # Переходим к следующему состоянию

# Обработчик для состояния age
@dp.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    student_data['age'] = message.text
    await message.reply("Введите ваш класс")
    await state.set_state(Form.class_name)  # Переходим к следующему состоянию

# Обработчик для состояния class_name
@dp.message(Form.class_name)
async def process_class(message: types.Message, state: FSMContext):
    student_data['class'] = message.text
    await message.reply("Введите урок, который нужно выполнить")
    await state.set_state(Form.lesson)  # Переходим к следующему состоянию

# Обработчик для состояния lesson
@dp.message(Form.lesson)
async def process_lesson(message: types.Message, state: FSMContext):
    student_data['lesson'] = message.text
    await message.reply("Введите задание")
    await state.set_state(Form.task)  # Переходим к следующему состоянию

# Обработчик для состояния task
@dp.message(Form.task)
async def process_task(message: types.Message, state: FSMContext):
    student_data['task'] = message.text
    await message.reply("Когда нужно выполнить задание? (в формате 'ДД.ММ.ГГГГ ЧЧ:ММ')")
    await state.set_state(Form.deadline)  # Переходим к следующему состоянию

# Обработчик для состояния deadline
@dp.message(Form.deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    try:
        # Парсим введенную дату
        deadline_time = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
        student_data['deadline'] = deadline_time
        await message.reply(f"Задание будет выполнено в {deadline_time.strftime('%d.%m.%Y %H:%M')}.")
        
        # Планируем выполнение задания
        await schedule_task(deadline_time)

        # Завершаем разговор
        await state.finish()
    except ValueError:
        await message.reply("Неверный формат даты. Пожалуйста, используйте формат 'ДД.ММ.ГГГГ ЧЧ:ММ'.")

async def schedule_task(deadline_time):
    # Рассчитываем разницу времени
    now = datetime.now()
    delta = (deadline_time - now).total_seconds()

    if delta < 0:
        await bot.send_message(student_data['phone'], "Это задание уже должно быть выполнено.")
    else:
        # Планируем выполнение уведомления через aioschedule
        schedule.every(delta).seconds.do(task_done)

async def task_done():
    # Когда время выполнения задания наступит, отправляется сообщение
    await bot.send_message(student_data['phone'], f"Задание для {student_data['name']} выполнено!")

# Асинхронная функция для проверки расписания
async def scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

# Основная функция для запуска бота
async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())  # Запускаем планировщик
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
