import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logger(name: str = None, log_file: str = "orders_api.log") -> logging.Logger:
    logger = logging.getLogger(name or __name__)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    file_handler = RotatingFileHandler(
        log_dir / log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = None) -> logging.Logger:
    return setup_logger(name)

