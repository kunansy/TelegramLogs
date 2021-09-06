from environs import Env


env = Env()
env.read_env('.env')

GRANTED_USERS = env.list('GRANTED_USERS', [])
DEVELOPER_USERNAME = env('DEVELOPER_USERNAME')

with env.prefixed('TELEGRAM_BOT_'):
    TELEGRAM_BOT_TOKEN = env('TOKEN')
