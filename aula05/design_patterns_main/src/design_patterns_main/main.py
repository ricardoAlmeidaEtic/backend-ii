from fastapi import FastAPI
import asyncio

app = FastAPI()

async def simulated_io_task_1():
    await asyncio.sleep(1)
    return "Data 1 fetched!"

async def simulated_io_task_2():
    await asyncio.sleep(2)
    return "Data 2 fetched!"

@app.get("/async-data")
async def get_data():
    return {"message": await asyncio.gather(simulated_io_task_1(), simulated_io_task_2())}

# Run using: uvicorn filename:app --reload