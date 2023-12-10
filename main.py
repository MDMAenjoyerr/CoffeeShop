import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = '6842731492:AAFxcqwAxWMVlk31OjShWgQFRUIZ-txioBI'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Клавиатура
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton("Список команд"))
menu.add(KeyboardButton("Меню"))
menu.add(KeyboardButton("🌍Где нас найти?🌍"))


# Список геолокаций кофеен
locations = [
    {"title": "Кофейня 1", "latitude": 55.7558, "longitude": 37.6176},
    {"title": "Кофейня 2", "latitude": 55.7505, "longitude": 37.6055},
    # Добавьте дополнительные кофейни, если необходимо
]

# Генерация клавиатуры с инлайн-кнопками для геолокаций
locations_keyboard = InlineKeyboardMarkup()
for location in locations:
    locations_keyboard.add(
        InlineKeyboardButton(text=f"{location['title']} 📍", callback_data=f"location:{location['latitude']}:{location['longitude']}")
    )


# Обработка команды /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Привет! Я бот кофейни. Напиши /menu чтобы увидеть меню.", reply_markup=menu)


# Обработка команды /help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer("Список команд:\n/start - начать работу с ботом\n/help - список команд\n/menu - посмотреть меню",
                         reply_markup=menu)


# Обработка команды /menu
@dp.message_handler(commands=['Меню'])
async def process_menu_command(message: types.Message):
    await message.answer("Меню с ценами на кофе:\n1. Эспрессо - $2\n2. Латте - $3\n3. Капучино - $4", reply_markup=menu)


# Обработка кнопки "Где нас найти?"
@dp.message_handler(lambda message: message.text == "Где нас найти?", content_types=types.ContentTypes.TEXT)
async def process_location_button(message: types.Message):
    await message.answer("Выбери кофейню, чтобы увидеть её местоположение:", reply_markup=locations_keyboard)


# Обработка инлайн-кнопок с геолокациями
@dp.callback_query_handler(lambda c: c.data.startswith('location'))
async def process_location_button(callback_query: types.CallbackQuery):
    _, latitude, longitude = callback_query.data.split(":")
    location_text = f"Вы выбрали кофейню по координатам:\nШирота: {latitude}\nДолгота: {longitude}"
    await bot.send_message(callback_query.from_user.id, location_text)


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)