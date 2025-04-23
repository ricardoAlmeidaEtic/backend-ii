from typer import Typer
from exporter import db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Typer app
app = Typer()

@app.command()
def generate_report(output_file: str = "report.csv"):
    """
    Generates a report from the 'processed_data' collection and saves it to a CSV file.

    Args:
        output_file (str): The name of the output CSV file (default: 'report.csv').
    """
    try:
        # Fetch data from the 'processed_data' collection
        collection = db.get_collection("processed_data")
        data = list(collection.find({}, {"_id": 0}))  # Exclude the MongoDB `_id` field

        if not data:
            logger.warning("No data found in the 'processed_data' collection.")
            return

        # Write data to a CSV file
        import csv
        with open(output_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        logger.info(f"Report generated successfully: {output_file}")
    except Exception as e:
        logger.error(f"Error generating report: {e}")

if __name__ == "__main__":
    app()