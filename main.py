#!/usr/bin/env python3
from aiogram import executor

from src import msg_handler
from src import bot_api


async def on_startup(*args):
    await bot_api.set_default_commands()
    await bot_api.notify_startup()


def main() -> None:
    bot_api.dp.loop.create_task(msg_handler.start_app())
    executor.start_polling(bot_api.dp, on_startup=on_startup)


if __name__ == '__main__':
    main()
