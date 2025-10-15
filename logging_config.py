"""
Настройка логирования для бота Netwell
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging():
    """Настройка логирования бота"""
    
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    logger.handlers.clear()
    
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    file_handler = RotatingFileHandler(
        logs_dir / 'bot.log',
        maxBytes=5*1024*1024,  
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    error_handler = RotatingFileHandler(
        logs_dir / 'errors.log',
        maxBytes=5*1024*1024,
        backupCount=3,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)
    
    # === КОНСОЛЬ: ТОЛЬКО ВАЖНОЕ ===
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)  
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # === ОТКЛЮЧАЕМ ЛИШНИЕ ЛОГИ БИБЛИОТЕК ===
    
    logging.getLogger('telegram').setLevel(logging.ERROR)
    logging.getLogger('telegram.ext').setLevel(logging.ERROR)
    
    logging.getLogger('httpx').setLevel(logging.ERROR)
    logging.getLogger('httpcore').setLevel(logging.ERROR)
    
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    
    return logger

def log_startup_info():
    """Логирование информации при старте"""
    logger = logging.getLogger(__name__)
    logger.warning("=" * 50)
    logger.warning("🚀 БОТ NETWELL ЗАПУЩЕН")
    logger.warning("=" * 50)

def log_shutdown_info():
    """Логирование информации при остановке"""
    logger = logging.getLogger(__name__)
    logger.warning("=" * 50)
    logger.warning("🛑 БОТ NETWELL ОСТАНОВЛЕН")
    logger.warning("=" * 50)