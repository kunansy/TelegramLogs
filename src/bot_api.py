import asyncio
from functools import wraps
from typing import Callable

from aiogram import Bot, Dispatcher, types

from src import _log_record, settings


loop = asyncio.get_event_loop()

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot, loop=loop)


def auth(func: Callable):
    @wraps(func)
    async def wrapped(msg: types.Message):
        if msg.from_user.username not in settings.GRANTED_USERS:
            return await msg.reply("I don't fucking know who are you, man")
        return await func(msg)
    return wrapped


async def send_log_record(log_record: _log_record.LogRecord) -> None:
    chat, msg = settings.TELEGRAM_BOT_CHAT_ID, str(log_record)
    await bot.send_message(chat, msg, parse_mode="markdown",
                           disable_web_page_preview=True)


@dp.message_handler(commands=['start'])
@auth
async def welcome(msg: types.Message) -> None:
    await msg.reply(
        "Hi there!\nI'm logs handler bot!\n"
        f"Developed by [him]({settings.DEVELOPER_USERNAME})",
        parse_mode="markdown", disable_web_page_preview=True)


@dp.message_handler()
@auth
async def echo(msg: types.Message) -> None:
    await msg.answer(msg.text)
