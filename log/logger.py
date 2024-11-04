import logging

logger = logging.getLogger()
formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")

# shipping target(s)
file_handler = logging.FileHandler('app.log')

file_handler.setFormatter(formatter)

logger.handlers = [file_handler,]

logger.setLevel(logging.INFO)