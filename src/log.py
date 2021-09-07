import logging
from typing import Literal

from src import settings


LOG_FMT = "{levelname:<10} [{asctime},{msecs:3.0f}] [PID:{process}] " \
          "[{filename}:{funcName}():{lineno}] {message}"
DATE_FMT = "%d.%m.%Y %H:%M:%S"

LOG_LEVEL = Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


logger = logging.getLogger('reports')
logger.setLevel(settings.LOGGER_LEVEL)

formatter = logging.Formatter(
    fmt=LOG_FMT, datefmt=DATE_FMT, style='{'
)


def add_stream_handler(_logger: logging.Logger,
                       level: LOG_LEVEL = 'DEBUG') -> None:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level)

    _logger.addHandler(stream_handler)


add_stream_handler(logger)
logger.info(f"Logger configured with level={logger.level}")
