import logging
import sys
from pythonjsonlogger import jsonlogger
from config import settings

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    
    # If the logger already has handlers, don't add more
    if logger.handlers:
        return logger

    log_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    log_handler.setFormatter(formatter)
    
    logger.addHandler(log_handler)
    logger.setLevel(settings.LOG_LEVEL)
    
    return logger

# Create a root logger instance
logger = setup_logger("api_pulse")
