import asyncio

async def task_function(name, delay):
    await asyncio.sleep(delay)
    return f"{name} completed"

async def main():
    task1 = asyncio.create_task(task_function("Task 1", 1))
    task2 = asyncio.create_task(task_function("Task 2", 2))
    results = await asyncio.gather(task1, task2)
    print(results)

asyncio.run(main())
