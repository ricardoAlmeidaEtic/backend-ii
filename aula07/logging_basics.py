import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log')

logging.info("This is an info message")
logging.warning("This is a warning message")
logging.error("This is an error message")
