import logging, sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_logger(name: str = "sales") -> logging.Logger:
    Path("logs").mkdir(exist_ok=True)
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)s | %(message)s")

    sh = logging.StreamHandler(sys.stdout); sh.setFormatter(fmt)
    fh = RotatingFileHandler("logs/run.log", maxBytes=5_000_000, backupCount=5)
    fh.setFormatter(fmt)
    logger.addHandler(sh); logger.addHandler(fh)
    return logger