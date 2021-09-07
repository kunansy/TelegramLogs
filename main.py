#!/usr/bin/env python3
from aiogram import executor

from src import msg_handler
from src.bot_api import dp


def main() -> None:
    dp.loop.create_task(msg_handler.start_app())
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
