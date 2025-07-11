# services/rich_logger.py

import logging
from rich.logging import RichHandler

logger = logging.getLogger("wastewise")
logger.setLevel(logging.DEBUG)

handler = RichHandler(rich_tracebacks=True, show_time=True, show_level=True)
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)

def log_info(msg: str):
    logger.info(f"ℹ️  {msg}")

def log_warn(msg: str):
    logger.warning(f"⚠️  {msg}")

def log_error(msg: str):
    logger.error(f"❌ {msg}")

def log_success(msg: str):
    logger.info(f"✅ {msg}")
