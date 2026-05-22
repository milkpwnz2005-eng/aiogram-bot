from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import aiosqlite

router = Router()

#----- Команды бота -----

@router.message(Command("start"))
async def start_command(message: Message):
    await init_db()
    await message.answer("Привет! Пропишите команду: /reg NAME, чтобы зарегистрироваться в боте.")    




@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Вот список команд, которые я поддерживаю:\n"
                         "/start - начать общение с ботом\n"
                         "/help - показать это сообщение\n" 
                         "/reg - зарегистрироваться в боте\n"
                         "Просто напиши мне, что ты хочешь сделать, и я постараюсь помочь!")
    



#----- Функция для работы с базой данных -----

DB_NAME = "bot_database.sqlite"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT
            )
        """)
        await db.commit()

async def add_user(user_id: int, username: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        await db.commit()


async def get_all_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        result = await cursor.fetchall()
    return result


@router.message(Command("reg"))
async def reg(message: Message):
    parts = message.text.strip().split(maxsplit=1)

    if len(parts) != 2 or not parts[1].strip():
        await message.answer("Введите команду верно. Пример: /reg Иван")
        return
    
    username = parts[1].strip()
    await add_user(message.from_user.id, username)

    await message.answer("Всё готово!")
   
@router.message(Command("users"))
async def users(message: Message):
    users = await get_all_users()

    if not users:
        await message.answer("Пользователи не найдены.")
        return

    text = "Пользователи:\n\n"
    for row_id, user_id, username in users:
        text += (
            f"ID записи: {row_id}\n"
            f"Telegram ID: {user_id}\n"
            f"Имя: {username or '—'}\n\n"
        )

    await message.answer(text, parse_mode="HTML")
