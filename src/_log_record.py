import datetime
from dataclasses import dataclass
from typing import Any, Optional


LOGGER_LEVELS = (
    'NOTSET', 'DEBUG', 'INFO',
    'WARNING', 'ERROR', 'CRITICAL'
)


@dataclass
class LogRecord:
    logger_name: str
    logger_level: str
    record_date: datetime.datetime
    where: Optional[str]
    message: str


def parse_response(response: dict[str, Any]) -> LogRecord:
    logger_level = response['logger_level']
    assert logger_level.upper() in LOGGER_LEVELS, "Invalid logger_level"

    return LogRecord(
        logger_name=str(response['logger_name']),
        logger_level=logger_level.upper(),
        record_date=datetime.datetime.fromisoformat(response['record_date']),
        where=response.get('where'),
        message=response['message']
    )
