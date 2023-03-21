from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import client_kb
from data_base import sqlite_db


# @dp.message_handler(commands=['start', 'help'])
from keyboards import kb_client


async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Давай вип'ємо кави!", reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply("Спілкування з ботом через ЛС, напишіть йому:\nhttps://t.me/Lovely_coffeBot")


# @dp.message_handler(commands=['Режим_роботи'])
async def coffee_open(message: types.Message):
    await bot.send_message(message.from_user.id, "Пн-Нд: Відчинено з 8:00 до 21:00")


# @dp.message_handler(commands=['Розташування'])
async def coffee_place(message: types.Message):
    await bot.send_message(message.from_user.id, "вулиця Хлібна, 4")


@dp.message_handler(commands=['Меню'])
async def coffee_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(coffee_open, commands=['Режим_роботи'])
    dp.register_message_handler(coffee_place, commands=['Розташування'])
    dp.register_message_handler(coffee_menu_command, commands=['Меню'])
