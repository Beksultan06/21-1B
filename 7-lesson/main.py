import aioschedule as schedule
import asyncio

async def task():
    print("Задача выполяется")

async def hello():
    print("Hello world")

async def start_task():
    schedule.every(1).seconds.do(hello)
    schedule.every(1).seconds.do(task)

    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

asyncio.run(start_task())