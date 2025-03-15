from sys import stderr
from loguru import logger
from config import settings


log_format = \
    "<green>{time:HH:mm:ss.SSSSS}</green> | " \
    "<level>{level: <7}</level> | " \
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

logger.remove()

logger.add(
    stderr,
    colorize=True,
    format=log_format,
    catch=True,
    diagnose=True
)

logger.add(
    settings.LOGS_PATH + "/logs_{time:YY-MM-DD}.log", level="INFO", format=log_format,
    rotation="00:00", retention="35 days", compression="zip"
)

logger.info("Logger is configured")
