# TelegramLogs
Dump some critical logs from services to Telegram bot

## Intro
To start use the bot handler one should create bot in TG with [@BotFather](https://t.me/BotFather),
create special method via which log messages would be sent to the bot and run the service with bot.

## Logger method
Your logger should have method like:
```python3
import logging
import json

import aiohttp


BOT_HANDLER_URL = "http://telegram_logs:2025/logs"


class Logger(logging.Logger):
    async def send_to_bot(self, 
                          msg: logging.LogRecord) -> None:
        log_record = {
            "logger_name": self.name,
            "logger_level": msg.levelname,
            "record_date": msg.asctime, # convert it to isoformat, otherwise an exception will be raised
            "where": f"{msg.module}: {msg.funcName}, {msg.lineno} line",
            "message": msg.message
        }
        data = json.dumps(log_record)
        
        timeout = aiohttp.ClientTimeout(20)
        async with aiohttp.ClientSession(timeout=timeout) as ses:
            try:
                await ses.post(BOT_HANDLER_URL, data=data)
            except Exception as e:
                self.log(30, f"TG bot doesn't work: {e}")
        
        self.log(msg.levelno, msg.message)
```

## `docker-compose` example
```yaml
version: '3'

services:
  telegram_logs:
    image: kunansy/telegram_logs
    environment:
      - TELEGRAM_BOT_TOKEN=<your bot token>
      - TELEGRAM_BOT_CHAT_IDS=42 # id of chats to where the bot will send handled messages

      - GRANTED_USERS=oh_its_my_chief,oh_its_me # which users might use the bot
      - DEVELOPER_USERNAME=https://github.com/kunansy # who created the bot
    entrypoint: ["python3", "main.py"]
    container_name: telegram_logs
    healthcheck:
      test: "exit 0"
    networks:
      - mainservice_net

# Connect the logger to main network to process logs from there.
networks:
  mainservice_net:
    external: true
```

## Credits
1. [GitHub](https://github.com/kunansy/TelegramLogs)
2. [DockerHub](https://hub.docker.com/r/kunansy/telegram_logs)
