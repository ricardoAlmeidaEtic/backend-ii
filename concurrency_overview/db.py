from pymongo import MongoClient
from api.settings import settings

config = Setting()

async def get_collection(name: str):
    """
    Asynchronously retrieves a MongoDB collection by name.
    
    Args:
        name (str): The name of the collection to retrieve.
    
    Returns:
        Collection: The MongoDB collection object.
    """
    client = MongoClient(config.MONGO_URI)  # Replace with your MongoDB URI
    db = client[config.MONGO_DB_NAME]       # Replace with your database name
    return db[name]