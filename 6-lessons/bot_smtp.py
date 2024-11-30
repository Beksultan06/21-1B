import aiosmtplib, logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from email.message import EmailMessage
from config import SMTP_USER, SMTP_PASSWORD, token

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = SMTP_USER
SMTP_PASSWORD = SMTP_PASSWORD

logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=token)
dp = Dispatcher()

async def send_email(to_emain, message_body):
    message = EmailMessage()
    message.set_content(message_body)
    message['Subject'] = 'Сообщение от бота'
    message['From'] = SMTP_USER
    message['To'] = to_emain

    try:
        logging.info(f'Отправка email на {to_emain}')
        await aiosmtplib.send(
            message,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USER,
            password=SMTP_PASSWORD
        )
        logging.info("Успешно отправлена")
    except Exception as e:
        logging.info("Ошибка", e)

@dp.message(Command("start"))
async def start(message:types.Message):
    await message.answer("Привет, введите почу которому хотите отправить сообщение!")

@dp.message(lambda message: "@gmail.com" in message.text)
async def email(message:types.Message):
    user_email = message.text
    await message.answer(f"Я отправлю сообщенеи на адрес {user_email}")

    email_message = 'Привет \n это сообщение отправлена через бота!'
    await send_email(user_email, email_message)
    await message.answer("Сообщение успешно отправлена!")

@dp.message(lambda message: '@' not in message.text)
async def error(message:types.Message):
    await message.answer("Пожалуйста введите правильный адрес почты")

async def main():
    await dp.start_polling(bot)

if __name__=='__main__':
    import asyncio
    asyncio.run(main())