from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router
import logging, asyncio, json
from config import token

bot = Bot(token=token)
dp = Dispatcher()

router = Router()

logging.basicConfig(level=logging.INFO)

student_file = 'student.json'

def save_student_data(student_data):
    try:
        with open(student_file, 'r') as f:
            students = json.load(f)
    except (FileExistsError, json.JSONDecodeError):
        students = []

    logging.info(f"Данные о студентах в начале {students}")

    students.append(student_data)

    with open(student_file, "w") as f:
        json.dump(students, f, indent=4)

    logging.info(f"Данные о студентах полсе записи {students}")

class Student(StatesGroup):
    name = State()
    age = State()
    specialty = State()

@router.message(Command('start'))
async def start(message: types.Message, state:FSMContext):
    await message.answer("Привет! как вас зовут???")
    await state.set_state(Student.name)

@router.message(Student.name)
async def name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f"Приятно познокомиться, {message.text}! Сколько вам лет!")
    await state.set_state(Student.age)

@router.message(Student.age)
async def age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await message.answer(f"Отлично, На какой специальности вы учитесь?")
        await state.set_state(Student.specialty)
    except ValueError:
        await message.answer("Пожалуйста введите корректный возраст(целое число).")

@router.message(Student.specialty)
async def specialty(message: types.Message, state:FSMContext):
    await state.update_data(specialty=message.text)

    student_data = await state.get_data()
    name = student_data['name']
    age = student_data['age']
    specialty = student_data['specialty']

    logging.info(f"Сохраняем данные")

    save_student_data({
        'name': name,
        'age': age,
        'specialty' : specialty
    })

    await message.answer(
        f"Информация о студенте: \n"
        f"Имя: {name}\n"
        f"Возраст: {age}\n"
        f"Специальность: {specialty}"
    )
    await state.clear()

@router.message(Command('students'))
async def lsit_student(message: types.Message):
    try:
        with open(student_file, 'r') as f:
            students = json.load(f)
    except (FileExistsError, json.JSONDecodeError):
        students = []

    logging.info(f"Данные о студентах {students}")

    if students:
        student_list = "\n".join([f"{i+1}. {student['name']}, {student['age']}, {student['specialty']}," for i, student in enumerate(students)] )
        await message.answer(f"Список студентов: \n{student_list}")
    else:
        await message.answer("Список студентов пуст!")

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__=='__main__':
    asyncio.run(main())