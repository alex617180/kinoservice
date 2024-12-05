# config/components/logging_config.py
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'django_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django_file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

class LevelFilter(logging.Filter):
    """
    A filter that passes only messages of a certain logging level
    """
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


# Функция для создания обработчиков
def create_handler(
        log_level_name:str,
        log_name:str,
        when:str='D',
        interval:int=5,
        backupCount:int=5,
        encoding:str='utf-8'
    ) -> logging.Handler:
    """
    Function to create a handler

    Args:
        log_level_name (str): Name of the log level.
        log_name (str): Name of the log.
        when (str): Type of interval.
        interval (int): Interval.
        backupCount (int): Backup count.
        encoding (str): Encoding.

    Returns:
        logging.Handler: Handler.
    """
    log_level = getattr(logging, log_level_name)
    file_path = os.path.join(BASE_DIR, 'logs', f'{log_name}_{log_level_name.lower()}.log')
    
    handler = TimedRotatingFileHandler(
        file_path,
        when=when,
        interval=interval,
        backupCount=backupCount,
        encoding=encoding
    )

    handler.setLevel(log_level)
    handler.addFilter(LevelFilter(log_level))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    return handler


def get_logger(name:str) -> logging.Logger:
    """
    Function to create a logger

    Args:
        name (str): Name of the logger.

    Returns:
        logger: Logger.
    """
    logger = logging.getLogger(name)
    # Set the logging level
    logger.setLevel(logging.DEBUG)

    # Create and add handlers
    log_levels = ['INFO', 'ERROR']
    for level in log_levels:
        handler = create_handler(level, name)
        logger.addHandler(handler)

    return logger

logger = get_logger('APP')