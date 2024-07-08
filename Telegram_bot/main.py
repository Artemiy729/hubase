import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import csv
import io

API_TOKEN = '6960881138:AAHXJYEgSeSsIZvB8ks-N2PxLrNINgdI6ik'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Кнопка для начала
start_button = KeyboardButton('Начать')
start_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(start_button)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(f"Привет, {message.from_user.first_name}!", reply_markup=start_kb)

@dp.message_handler(lambda message: message.text == 'Начать')
async def ask_for_companies(message: types.Message):
    await message.reply("Пожалуйста, введите список компаний, одна строка - одна компания:")

@dp.message_handler()
async def process_companies(message: types.Message):
    companies = message.text.split('\n')
    # Моковое API - здесь просто имитируем поиск
    # В реальном случае мы бы делали запрос к API и обрабатывали ответ
    results = {company: "No data found" for company in companies}

    # Создаем CSV файл в памяти
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Company', 'Result'])
    for company, result in results.items():
        writer.writerow([company, result])
    
    output.seek(0)
    await message.reply_document(types.InputFile(output, 'results.csv'), caption="Вот ваш CSV файл с результатами.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)