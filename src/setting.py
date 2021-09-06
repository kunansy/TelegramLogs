from environs import Env


env = Env()
env.read_env('.env')

with env.prefixed('TELEGRAM_BOT_'):
    TELEGRAM_BOT_TOKEN = env('TOKEN')
