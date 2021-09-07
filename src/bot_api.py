import asyncio
from functools import partial

from aiogram import Bot, Dispatcher, types

from src import _log_record, settings


loop = asyncio.get_event_loop()

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot, loop=loop)

allow_access = lambda msg: msg.from_user.username in settings.GRANTED_USERS
message_handler = partial(dp.message_handler, allow_access)


async def send_log_record(log_record: _log_record.LogRecord) -> None:
    await bot.send_message(
        settings.TELEGRAM_BOT_CHAT_ID, text)


@message_handler(commands=['start'])
async def welcome(msg: types.Message) -> None:
    await msg.reply(f"Hi there!\nI'm logs handler bot!\n"
                    f"Developed by @{settings.DEVELOPER_USERNAME}")


@message_handler()
async def echo(msg: types.Message) -> None:
    await msg.answer(msg.text)
