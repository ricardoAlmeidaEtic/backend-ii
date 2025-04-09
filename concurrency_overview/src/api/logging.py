

import logging


def setup_logging(level: int = logging.INFO):
    """Setup logging for the application. Logging format has process name and thread name"""
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(processName)s - %(threadName)s - %(name)s - %(message)s")

    