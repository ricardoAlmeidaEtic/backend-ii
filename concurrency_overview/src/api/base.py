from fastapi import FastAPI

from api import settings
from api.logging import setup_logging

config = settings.BaseSettings()

api = FastAPI(
    title="Concurrency Overview",
    description="A simple API to demonstrate the differences between concurrency models.",
    version="0.1.0",
)

setup_logging()


async def fetch_and_save() -> Dict[str, str]:
    """Fetches data from FakerAPI and saves it to MongoDB."""
    try:
        response = requests.get(FAKER_API_URL)
        response.raise_for_status()
        data = response.json()["data"]
        await db.raw_data.insert_many(data)
        logger.info(f"Fetched and saved {len(data)} items.")
        return {"message": f"Fetched and saved {len(data)} items."}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error saving to database: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_all_raw_data/")
async def get_all_raw_data() -> List[Dict[str, Any]]:
    """Retrieves all raw data from MongoDB."""
    try:
        data = await db.raw_data.find().to_list(length=None)
        return data
    except Exception as e:
        logger.error(f"Error retrieving data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# data_pipeline/worker.py
import logging
import os
from typing import List, Dict, Any

import typer
import asyncio
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import httpx

load_dotenv()

app = typer.Typer()

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "data_pipeline")
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

API_URL = "http://api:8000/get_all_raw_data/"

async def fetch_data_from_api() -> List[Dict[str, Any]]:
    """Fetches data from the API."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching data: {e}")
        return []
    except Exception as e:
        logger.error(f"Error fetching data from API: {e}")
        return []

async def process_and_save_data(data: List[Dict[str, Any]]) -> None:
    """Processes and saves data to MongoDB."""
    if not data:
        return
    processed_data = []
    for item in data:
        processed_item = {
            "firstname": item["firstname"],
            "lastname": item["lastname"],
            "email": item["email"],
            "phone": item["phone"]
        }
        processed_data.append(processed_item)

    try:
        await db.processed_data.insert_many(processed_data)
        logger.info(f"Processed and saved {len(processed_data)} items.")
    except Exception as e:
        logger.error(f"Error saving processed data: {e}")

async def export_to_csv() -> None:
    """Exports processed data to CSV."""
    try:
        data = await db.processed_data.find().to_list(length=None)
        df = pd.DataFrame(data)
        df.to_csv("processed_data.csv", index=False)
        logger.info("Exported processed data to CSV.")
    except Exception as e:
        logger.error(f"Error exporting to CSV: {e}")

@app.command()
def process():
    """Fetches, processes, and saves data."""
    asyncio.run(main_process())

async def main_process():
    """main process."""
    data = await fetch_data_from_api()
    await process_and_save_data(data)

@app.command()
def export():
    """Exports processed data to CSV."""
    asyncio.run(export_to_csv())

if __name__ == "__main__":
    app()