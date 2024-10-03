# Savollar
# 1. Aiogram kutubxonasi nima va u Telegram botlarini yaratishda nima uchun ishlatiladi?

# Aiogram — bu Telegram botlari uchun ishlab chiqilgan Python kutubxonasi bo'lib, u asinxron kodlashni qo'llab-quvvatlaydi va Telegram API bilan ishlashni soddalashtiradi.
# U foydalanuvchilar bilan muloqot, xabarlarni qayta ishlash, tugmalar yaratish kabi ko'plab qulay imkoniyatlarni taqdim etadi.

#  2. Aiogram yordamida botni qanday yaratish mumkin?

# from aiogram import Bot, Dispatcher, filters, types, F
# import asyncio
#
#
# from config import TOKEN
# import reply, inline
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.fsm.context import FSMContext
# from database import Database
# from aiogram.types import CallbackQuery

#  3. Botni aiogram’ga ulash uchun BotFather’dan qanday turdagi token olish kerak?

# api token orqali

#  4. Aiogram yordamida foydalanuvchilardan kiruvchi xabarlarni qanday qayta ishlash mumkin?
# Aiogram’da foydalanuvchilardan kelgan xabarlarni qayta ishlash uchun @dp.message_handler dekoratoridan foydalaniladi.
# Xabarlar turiga qarab, tegishli funksiyalar yoziladi.

# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(message.text)


#  5. Bot orqali foydalanuvchiga matnli xabar qanday yuboriladi?

# Foydalanuvchiga matnli xabar yuborish uchun message.answer() funksiyasidan foydalaniladi:

# await message.answer(" matnli xabar.")


#  6. Aiogram yordamida yana qanday turdagi xabarlarni (foto, audio, video va h.k.) yuborish mumkin?

# Aiogram yordamida quyidagi turdagi fayllarni yuborish mumkin:
#
# Foto: message.answer_photo()
# Audio: message.answer_audio()
# Video: message.answer_video()
# Hujjat: message.answer_document()

#  7. Bot orqali foydalanuvchi bilan muloqot qilish uchun tugmachali klaviatura qanday amalga oshiriladi?

# ReplyKeyboardMarkup  orqali

# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
#
# keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
# button = KeyboardButton('Birinchi tugma')
# keyboard.add(button)
#
# await message.answer("Tanlang", reply_markup=keyboard)


#  8. Chat va xabar yuborgan foydalanuvchi haqida qanday ma'lumot olsam bo'ladi?

# message.from_user orqali

# username = message.from_user.username


#  9. SQLite3 ma'lumotlar bazasi nima va unda qanday asosiy operatsiyalarni bajarish mumkin?

# SQL ma'lumotlar bazasi  ma'lumotlarni qo'shish  va o'chirish va yangilash mumkin



#  10. Pythonda SQLite3 ma'lumotlar bazasini qanday ulash va yaratish mumkin?

# sqlite3 kutubxonasi orqali ulash mumkin:

# import sqlite3



#  11. Bot foydalanuvchilari haqidagi ma'lumotlarni saqlash uchun jadval yaratish uchun qanday SQL so'rovlarini bajarish kerak?

# Bot foydalanuvchilari uchun jadval yaratish:

# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY,
#     name TEXT,
#     age INTEGER,
#     phone TEXT
# );




#  12. Bot orqali ro'yxatdan o'tishda SQLite3 ma'lumotlar bazasiga yangi foydalanuvchi qanday qo'shiladi?

# cursor.execute("INSERT INTO users (id, name, age, phone) VALUES (?, ?, ?, ?)", (user_id, name, age, phone))
# conn.commit()


#  13. SQLite3 ma'lumotlar bazasida foydalanuvchi ma'lumotlarini qanday yangilash mumkin, masalan, profil o'zgarganda?

# UBDATE ORQALI


#  14. SQLite3 ma'lumotlar bazasi bilan ishlashda ma'lumotlar xavfsizligini qanday ta'minlash mumkin?

# hamma userga limit berish

#  15. GPT-3 dan aiogram kutubxonasi bilan birgalikda ijodiy bot yaratish uchun qanday foydalanish mumkin?

# pip install openai orqali
# import openai


# Mini-amaliy vazifa:
# Foydalanuvchidan matnli xabar oladigan va ijodiy javob bilan javob beradigan mini-bot yarating.  Aiogramda suhbatlar tarixini saqlash uchun “SQLite3” dan foydalaning. Bot bir necha turdagi xabarlarga javob bera olishi kerak, masalan, “salom”, “qalaysan?”, “menga hazil ayt”. Har bir savolning ma'lumotlar bazasidan o'ziga xos javobi bo'lishi kerak.
# #

import sqlite3
from aiogram import Bot, Dispatcher, types
import asyncio

TOKEN = "7914574662:AAFAXegyn1NPbmHsjUXFFRSkoVg6KvuoF6s"
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)


conn = sqlite3.connect('bot.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    question TEXT,
                    answer TEXT
                )''')
conn.commit()


@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    user_text = message.text.lower()

    cursor.execute("SELECT answer FROM users WHERE question = ?", (user_text,))
    result = cursor.fetchone()

    if result:
        await message.answer(result[0])
    else:
        if user_text == "salom":
            response = "Salom! Qalaysiz?"
        elif user_text == "qalaysan?":
            response = "Yaxshi, sizchi?"
        elif user_text == "menga hazil ayt":
            response = "Ikkita pomidor ko'chada yuribdi, biri ikkinchisiga: 'Tomatol!'"
        else:
            response = "Bunday savolga hali javobim yo'q."

        cursor.execute("INSERT INTO users (question, answer) VALUES (?, ?)", (user_text, response))
        conn.commit()

        await message.answer(response)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())