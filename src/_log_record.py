import datetime
from dataclasses import dataclass
from typing import Any, Optional


LOGGER_LEVELS = (
    'NOTSET', 'DEBUG', 'INFO',
    'WARNING', 'ERROR', 'CRITICAL'
)


def _format_date(date: datetime.datetime) -> str:
    return date.strftime("%d.%m.%Y %H:%M:%S.%f")


@dataclass
class LogRecord:
    logger_name: str
    logger_level: str
    record_date: datetime.datetime
    where: Optional[str]
    message: str

    def format(self) -> str:
        is_where = bool(self.where)

        return f"{self.logger_name}: *{self.logger_level}*\n\n" \
               f"When: {_format_date(self.record_date)}\n" \
               f"{'Where: ' * is_where}{self.where or ''}\n" \
               f"What: _{self.message}_"

    def __str__(self) -> str:
        return self.format()


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
