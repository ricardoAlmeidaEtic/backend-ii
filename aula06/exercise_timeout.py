import asyncio

async def task_with_timeout(name, delay):
    try:
        return await asyncio.wait_for(task_function(name, delay), timeout=1.5)
    except asyncio.TimeoutError:
        return f"{name} timed out"

async def task_function(name, delay):
    await asyncio.sleep(delay)
    return f"{name} completed"

async def main():
    tasks = [
        asyncio.create_task(task_with_timeout("Task 1", 1)),
        asyncio.create_task(task_with_timeout("Task 2", 2))
    ]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
