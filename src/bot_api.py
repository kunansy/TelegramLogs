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


async def send_msg(chat_id: int,
                   msg: str) -> None:
    try:
        await bot.send_message(
            chat_id, msg,
            disable_web_page_preview=True
        )
    except bex.BotBlocked:
        logger.error("[%s]: Bot blocked", chat_id)
    except bex.ChatNotFound:
        logger.error("[%s]: Chat not found", chat_id)
    except bex.RetryAfter as e:
        logger.error("[%s]: Flood limit exceeded. Sleep %ss.",
                     chat_id, e.timeout)
        await asyncio.sleep(e.timeout)
        return await send_msg(chat_id, msg)
    except bex.UserDeactivated:
        logger.error("[%s]: User deactivated", chat_id)
    except bex.TelegramAPIError:
        logger.exception("[%s]: Failed", chat_id)
    else:
        logger.info("[%s]: Success", chat_id)


async def set_default_commands() -> None:
    await bot.set_my_commands([
        types.BotCommand("start", "Start the bot and get info"),
        types.BotCommand("info", "Start the bot and get info"),
        types.BotCommand("healthcheck", "Test the bot is alive"),
    ])


async def notify_startup() -> None:
    if settings.NOTIFY_ON_STARTUP is False:
        return

    for admin_id in settings.ADMIN_IDS:
        await send_msg(admin_id, "Bot started")


def auth(func: Callable):
    @wraps(func)
    async def wrapped(msg: types.Message):
        if msg.from_user.username not in settings.GRANTED_USERS:
            return await msg.reply("I don't fucking know who are you, man")
        if msg.from_user.is_bot is True:
            return await msg.reply("You are a bot, I will not work with you")
        return await func(msg)
    return wrapped


async def send_log_record(log_record: _log_record.LogRecord) -> None:
    for chat_id in settings.TELEGRAM_BOT_CHAT_IDS:
        await send_msg(chat_id, log_record.format())


@dp.message_handler(commands=['start', 'info'])
@auth
async def welcome(msg: types.Message) -> None:
    await msg.reply(
        "Hi there\! I'm logs handler bot\!\n\n"
        f"Developer: [URL]({settings.DEVELOPER_USERNAME})\n"
        f"chat\_id: {msg.chat.id}\n",
        disable_web_page_preview=True,
        parse_mode=types.ParseMode.MARKDOWN_V2
    )


@dp.message_handler(commands=['healthcheck'])
@auth
async def echo(msg: types.Message) -> None:
    await msg.reply("I'm alive")
