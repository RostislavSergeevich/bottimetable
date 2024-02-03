
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

TOKEN = "6671588692:AAFnvr6xVE_YOjzb7rfmcZqB3ocmMuy1O0s"
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Создаем inline клавиатуру для выбора дней недели
def create_days_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    buttons = [types.InlineKeyboardButton(text=day, callback_data=day) for day in days]
    keyboard.add(*buttons)
    return keyboard
    
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = ['Класс 1', 'Класс 2', 'Класс 3']  # Замените на реальные классы
    keyboard.add(*buttons)
  
    await message.answer("Выбери класс:", reply_markup=keyboard)
    
@dp.message_handler()
async def get_day(message: types.Message):
    if message.text in ['Класс 1', 'Класс 2', 'Класс 3']:
        # Сохраняем выбранный класс в хранилище
        storage = dp.get_current().data
        storage['class'] = message.text
        
        await message.answer("Выбери день недели:", reply_markup=create_days_keyboard())

@dp.callback_query_handler(lambda c: True)
async def get_schedule(callback_query: types.CallbackQuery):
    day_of_week = callback_query.data
    
    # Получаем выбранный класс из хранилища
    storage = dp.get_current().data
    class_number = storage.get('class')

    if class_number and day_of_week:
        schedule_photo_path = f'{class_number}_{day_of_week.lower()}.jpg'  # Путь к фото расписания для конкретного класса и дня

        with open(schedule_photo_path, 'rb') as photo:
            await bot.send_photo(callback_query.from_user.id, photo)
            storage.clear()

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
