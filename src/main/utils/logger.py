from logging import getLogger
from logging import StreamHandler, Formatter, Logger
from logging import INFO

def get_logger(name: str) -> Logger:
    logger = getLogger(name)
    logger.setLevel(INFO)

    handler = StreamHandler()
    handler.setFormatter(Formatter(f"%(asctime)s - {name} - %(levelname)s - %(message)s"))

    logger.addHandler(handler)
    logger.propagate = False  # don’t also log through root
    return logger

