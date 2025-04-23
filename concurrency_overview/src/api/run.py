

config = Setting();

api = FastAPI(
    title="Concurrency Overview API",
    description="API for concurrency overview",
    version="0.1.0",
)

setup_logging()
logger = logging.getLogger(__name__)

@api.post

@api.get("/fetch_and_save/")
async def fetch_and_save():
    """
    Fetch data from FakerAPI and save it to MongoDB
    """
    try:
        response = requests.get(FAKER_API_URL)
        response.raise_for_status()
        data = response.json()["data"]
        db = await get_collection("raw_data")
        await db.insert_many(data)
        logger.info(f"Fetched and saved {len(data)} items.")
        return {"message": f"Fetched and saved {len(data)} items."}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error saving to database: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@api.get("/get_raw_data/")
async def get_raw_data()->list[dict]:
    """
    Get raw data from the database
    """
    try:
        db = await get_collection("raw_data")
        data = await db.find().to_list(1000)
        return data
    except Exception as e:
        logger.error(f"Error getting raw data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")