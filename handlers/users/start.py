import random
from logging import Logger

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from data.People import array_users, find_name
from keyboards.default.contact_buttons import contact
from keyboards.inline.check_keyboard import check
from loader import dp

pop_user = None


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await message.answer("Сейчас ты узнаешь, кому будешь дарить подарок!🤫\n"
                         "Но для начала ты должен поделиться своим номером, дабы тебе не попался твой же пользователь",
                         reply_markup=contact)


@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def show_info(message: types.Message):
    global pop_user
    if (len(array_users) != 0):
        contact = message.contact
        await message.answer("Спасибо, теперь ты себе не попадёшься...", reply_markup=ReplyKeyboardRemove())
        await message.answer("Жеребьёвка была проведена...\nИнтересно, кто же тебе попался?", reply_markup=check)
        user = random.choice(array_users)
        pop_user = find_name(message.contact["phone_number"])
    else:
        await message.answer("Прости, но больше нет людей кому можно было бы отправить подарок")


@dp.callback_query_handler(text="check")
async def def_check(call: CallbackQuery):
    global pop_user
    user = random.choice(array_users)

    await call.message.answer("Поздравляю, вот данные твоего тайного друга:")
    await call.message.answer(f"<b>ФИО</b>: {user[0]}\n"
                              f"<b>Телефон</b>: {user[1]}\n"
                              f"<b>Адрес</b>: {user[2]}\n"
                              f"<b>Индекс</b>: {user[3]}\n"
                              f"<b>ВК</b>: {user[4]}")
    print(f"Пользователю {call.from_user.full_name} достался {user[0]}")

    await call.message.edit_reply_markup()
    if (pop_user != None):
        array_users.append(pop_user)
        array_users.pop(array_users.index(user))
    else:
        array_users.pop(array_users.index(user))

    file = open("info_about_users.txt", "a+")
    file.write(f"{call.from_user.full_name} - {user[0]}\n")
    file.close()
