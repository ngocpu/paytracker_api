import logging
from logging.handlers import RotatingFileHandler 
from .global_seting import global_settings
def setup_logger():
    logger = logging.getLogger(global_settings.app_name)
    logger.setLevel(getattr(logging, global_settings.log_level.upper(), logging.INFO))
    
    # avoid duplicate handlers
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, global_settings.log_level.upper(), logging.INFO))
        
        file_handler = RotatingFileHandler(
            'src/logs/app.log', maxBytes=10*1024*1024, backupCount=5
        )
        file_handler.setLevel(getattr(logging, global_settings.log_level.upper(), logging.INFO))
        
        # define log format
        log_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        console_handler.setFormatter(log_format)
        file_handler.setFormatter(log_format)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

logger = setup_logger()