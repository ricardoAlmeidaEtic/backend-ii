import asyncio

async def rate_limited_task(semaphore, name):
    async with semaphore:
        print(f"{name} started")
        await asyncio.sleep(1)
        print(f"{name} completed")

async def main():
    semaphore = asyncio.Semaphore(2)  # Limit to 2 tasks per second
    tasks = [rate_limited_task(semaphore, f"Task {i}") for i in range(5)]
    await asyncio.gather(*tasks)

asyncio.run(main())
