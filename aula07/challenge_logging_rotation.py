import logging
from logging.handlers import TimedRotatingFileHandler

handler = TimedRotatingFileHandler("app.log", when="midnight", interval=1)
handler.suffix = "%Y-%m-%d"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[handler])

logging.info("This is an info message")
