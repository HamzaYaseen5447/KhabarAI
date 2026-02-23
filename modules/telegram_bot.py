from telegram import Bot
import asyncio

async def _send_message_async(bot_token: str, chat_id: str, text: str):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=text)

async def _send_audio_async(bot_token: str, chat_id: str, audio_file_path: str):
    bot = Bot(token=bot_token)
    with open(audio_file_path, "rb") as audio_file:
        await bot.send_audio(chat_id=chat_id, audio=audio_file)

def send_telegram_message(bot_token: str, chat_id: str, text: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(_send_message_async(bot_token, chat_id, text))
    finally:
        loop.close()

def send_telegram_audio(bot_token: str, chat_id: str, audio_file_path: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(_send_audio_async(bot_token, chat_id, audio_file_path))
    finally:
        loop.close()