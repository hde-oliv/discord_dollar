import sys

from loguru import logger


def get_logger():
    logger_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS ZZ}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
        "- <level>{message}</level>"
    )
    logger.remove()

    logger.add(sys.stderr, level="DEBUG", format=logger_format)
    logger.add(
        "./data/execution.log",
        level="INFO",
        enqueue=True,
        format=logger_format,
    )

    return logger
