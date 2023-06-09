from aiogram import types, Dispatcher
import json
import string
from create_bot import dp


# @dp.message_handler()
async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(" ")}\
            .intersection(set(json.load(open("cenz1.json")))) != set():
        await message.reply('Матюки тут заборонені Пиздюк!')
        await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
