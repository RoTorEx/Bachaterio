import logging
import sys
from logging import Logger


def build_logger(init_file_name: str) -> Logger:
    """Build custom logger."""
    logger = logging.getLogger(init_file_name)

    logging.basicConfig(
        level=logging.DEBUG,
        datefmt="%y-%m-%d %H:%M:%S",
        format="[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
        handlers=[
            logging.FileHandler(filename="src/bot.log", mode="a"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logger
