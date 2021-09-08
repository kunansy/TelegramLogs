import asyncio
from functools import wraps
from typing import Callable

from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions as bex

from src import _log_record, settings
from src.log import logger

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
    for chat_id in settings.TELEGRAM_BOT_CHAT_IDS:
        try:
            await bot.send_message(
                chat_id, log_record.format(),
                parse_mode="markdown", disable_web_page_preview=True
            )
        except bex.BotBlocked:
            logger.error("Bot blocked")
        except bex.ChatNotFound:
            logger.error("Chat not found")
        except bex.RetryAfter as e:
            logger.error(f"Target [{chat_id}]: Flood limit is exceeded. "
                         f"Sleep {e.timeout} seconds.")
            await asyncio.sleep(e.timeout)
            return await send_log_record(log_record)
        except bex.UserDeactivated:
            logger.error(f"Target [ID:{chat_id}]: user is deactivated")
        except bex.TelegramAPIError:
            logger.exception(f"Target [ID:{chat_id}]: failed")
        else:
            logger.info(f"Target [ID:{chat_id}]: success")


@dp.message_handler(commands=['start'])
@auth
async def welcome(msg: types.Message) -> None:
    await msg.reply(
        "Hi there!\nI'm logs handler bot!\n"
        f"Developed by [him]({settings.DEVELOPER_USERNAME})",
        parse_mode="markdown", disable_web_page_preview=True)


@dp.message_handler(commands=['echo'])
@auth
async def echo(msg: types.Message) -> None:
    await msg.answer(msg.text)
