import os

from environs import Env


env = Env()

# username of people who can access the bot
GRANTED_USERS = env.list('GRANTED_USERS', [])
ADMIN_IDS = env.list('ADMIN_ID', [])
DEVELOPER_USERNAME = env('DEVELOPER_USERNAME', "https://github.com/kunansy")
NOTIFY_ON_STARTUP = env.bool('NOTIFY_ON_STARTUP', True)

LOGGER_LEVEL = env.log_level('LOGGER_LEVEL', 'DEBUG')

DATE_FORMAT = "%d.%m.%Y %H:%M:%S.%f"

with env.prefixed('TELEGRAM_BOT_'):
    TELEGRAM_BOT_TOKEN = env('TOKEN')
    # TODO: ContextVar or db or another thing
    TELEGRAM_BOT_CHAT_IDS = env.list('CHAT_IDS')

LOG_MSG_HANDLER_HOST = '0.0.0.0'
LOG_MSG_HANDLER_PORT = 2025

os.environ.clear()