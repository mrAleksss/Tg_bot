from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from data_base import sqlite_db
from create_bot import dp, bot
from keyboards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, callback_query

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# Отримуємо ID теперішнього модератора
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Що треба, Повелитель???', reply_markup=admin_kb.button_case_admin)
    await message.delete()


# Початок діалога загрузки нового пункта меню
# @dp.message_handler(commands='Завантажити', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Завантаж фото')


# Вихід із станів
# @dp.message_handler(state="*", commands='відміна')
# @dp.message_handler(Text(equals='відміна', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('ok')


# Ловимо першу відповідь і записуємо в словник
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Тепер тапни назву')


# Ловимо другу відповідь
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Опиши, що бачиш')


# Ловимо третю відповідь
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Вкажи ціну')


# Ловимо останню відповідь і використовуємо отримані данні
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        await sqlite_db.sql_add_command(state)
        await state.finish()


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} видалена.', show_alert=True)


# @dp.message_handler(commands='Видалити')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f"{ret[1]}\nОпис: {ret[2]}\nЦіна {ret[-1]}")
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Видалити {ret[1]}', callback_data=f'del {ret[1]}')))


# @dp.message_handler(lambda message: 'кава' or 'кофе' or 'замовити' or 'заказать' in message.text)
# async def order(message: types.Message):
#     await message.answer('Ви можете замовити смачну каву завітавши до на за адресою Хлібна,4\
#      \nАбо подзвонивши за номером068xxxxxxx')



# Реєструємо хендлери
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands='Завантажити', state=None)
    dp.register_message_handler(cancel_handler, Text(equals='відміна', ignore_case=True), state="*")
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, state="*", commands='відміна')
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_item, commands='Видалити')
    # dp.register_message_handler(order, lambda message: 'кава' or 'кофе' or 'замовити' or 'заказать' in message.text)





