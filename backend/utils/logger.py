import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CoordinatorAI")

def log_message(message):
    logger.info(message)
