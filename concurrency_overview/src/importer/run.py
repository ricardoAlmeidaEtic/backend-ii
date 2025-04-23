from typer import
from multiprocessing import cpu_count
from exporter import db

api_endpoint = "http://api:8000/fetch"
raw_endpoint = "http://api:8000/get_raw_data/"
setup_logging()

app = Typer()

def collect_data():
    try:
        response = request.get(api_endpoint)
        response.raise_for_status()
        data = response.json()["data"]
        db.get_collection("raw_data").insert_many(data)
    except Exception as e:
        logger.error(f"Error collecting data: {e}")
        return None

def process_data():
    try:
        response = request.post(api_endpoint)
        response.raise_for_status()
        data = response.json()["data"]
        new_data = []
        for item in data:
            # Process the item as needed
            new_data.append({
                "firstname": item["firstname"],
                "lastname": item["lastname"],
                "email": item["email"],
                "phone": item["phone"]
            })
        db.get_collection("processed_data").insert_many(new_data)
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        return None

@app.command()
def process(total:int,run_process:int = cpu_count):
    assert num_processes <= cpu_count(), "Number of processes exceeds CPU count"
    with ThreadPoolExecutor(max_workers=num_processes) as executor:
        for _ in range.submit(1, total):
            executor.submit(process_data)

    logger.info("processed!")