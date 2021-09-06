import asyncio
from functools import partial

from aiogram import Bot, Dispatcher, executor, types

from src import settings, mesages_listener


loop = asyncio.get_event_loop()

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot, loop=loop)

allow_access = lambda msg: msg.from_user.username in settings.GRANTED_USERS
message_handler = partial(dp.message_handler, allow_access)


@message_handler(commands=['start'])
async def welcome(msg: types.Message) -> None:
    await msg.reply(f"Hi there!\nI'm logs handler bot!\n"
                    f"Developed by @{settings.DEVELOPER_USERNAME}")


@message_handler()
async def echo(msg: types.Message) -> None:
    await msg.answer(msg.text)


def main() -> None:
    dp.loop.create_task(mesages_listener.socket_listener())
    executor.start_polling(dp, skip_updates=True)
