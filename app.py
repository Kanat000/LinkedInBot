from aiogram import executor

from config import dbName
from database import dbConnection
from handlers.bot_service import dp

if __name__ == '__main__':
    dbConnection.Sqlite(dbName).create_user_table()
    executor.start_polling(dp)
