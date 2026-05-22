import os
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers.routes import *

dotenv_path = Path(__file__).resolve().parent / ".env"
if not dotenv_path.exists():
    raise FileNotFoundError(f".env file not found at {dotenv_path}")

load_dotenv(dotenv_path=dotenv_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN or BOT_TOKEN == "your_telegram_bot_token_here":
    raise RuntimeError("BOT_TOKEN is not set in .env. Set BOT_TOKEN in .env to your Telegram bot token.")

async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    print("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
