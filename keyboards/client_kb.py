from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


b1 = KeyboardButton('/Меню')
b2 = KeyboardButton('/Розташування')
b3 = KeyboardButton('/Режим_роботи')
# b4 = KeyboardButton('Поділитися номером', request_contact=True)
# b5 = KeyboardButton('Відправити свою локацію', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1).add(b2).add(b3)


