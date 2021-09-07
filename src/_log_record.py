import datetime
from dataclasses import dataclass
from typing import Any, Optional

from src import exceptions


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


def _parse_response(response: dict[str, Any]) -> LogRecord:
    logger_level = str(response['logger_level']).upper()

    return LogRecord(
        logger_name=str(response['logger_name']),
        logger_level=logger_level,
        record_date=datetime.datetime.fromisoformat(response['record_date']),
        where=response.get('where'),
        message=response['message']
    )


def parse_response(response: dict[str, Any]) -> LogRecord:
    try:
        return _parse_response(response)
    except (KeyError, ValueError) as e:
        raise exceptions.InvalidJSONFormat(e)
