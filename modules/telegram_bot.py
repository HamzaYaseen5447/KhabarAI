import asyncio
import nest_asyncio
from telegram import Bot

nest_asyncio.apply()

async def _send_message_async(bot_token: str, chat_id: str, text: str):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=text)

async def _send_audio_async(bot_token: str, chat_id: str, audio_file_path: str):
    bot = Bot(token=bot_token)
    with open(audio_file_path, "rb") as audio_file:
        await bot.send_audio(chat_id=chat_id, audio=audio_file)

def send_telegram_message(bot_token: str, chat_id: str, text: str):
    asyncio.run(_send_message_async(bot_token, chat_id, text))

def send_telegram_audio(bot_token: str, chat_id: str, audio_file_path: str):
    asyncio.run(_send_audio_async(bot_token, chat_id, audio_file_path))