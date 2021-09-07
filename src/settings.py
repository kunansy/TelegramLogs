from environs import Env


env = Env()
env.read_env('.env')

# username of people who can access the bot
GRANTED_USERS = env.list('GRANTED_USERS', [])
DEVELOPER_USERNAME = env('DEVELOPER_USERNAME')
LOGGER_LEVEL = env.log_level('LOGGER_LEVEL', 'DEBUG')

with env.prefixed('TELEGRAM_BOT_'):
    TELEGRAM_BOT_TOKEN = env('TOKEN')
    # TODO: ContextVar or db or another thing
    TELEGRAM_BOT_CHAT_ID = env.int('CHAT_ID')

LOG_MSG_HANDLER_HOST = '127.0.0.1'
LOG_MSG_HANDLER_PORT = 2025
