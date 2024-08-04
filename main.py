import telebot
from config import TOKEN
from handlers import start_handler, language_selection_handler, registration_handler, handle_registration_steps
from admin_panel import admin_panel_handler, handle_admin_commands

# Botni yaratish
bot = telebot.TeleBot(TOKEN)

# /start komandasini qabul qilish
@bot.message_handler(commands=['start'])
def handle_start(message):
    start_handler(message)

# Til tanlashni boshqarish
@bot.message_handler(func=lambda message: message.text.lower() in ["o'zbekcha", "русский"])
def handle_language_selection(message):
    language_selection_handler(message)

# Ro'yxatdan o'tishni boshqarish
@bot.message_handler(func=lambda message: message.text.lower() == 'kurslarimiz')
def handle_courses(message):
    registration_handler(message)

# Admin panelga kirish
@bot.message_handler(func=lambda message: message.text.lower() == 'admin panel')
def handle_admin_panel(message):
    admin_panel_handler(message)

# Admin uchun komandalarga javob berish
@bot.message_handler(func=lambda message: message.text.lower() in [
    'kurs qo\'shish',
    'kurs o\'chirish',
    'foydalanuvchilarni ko\'rish',
    'reklama yuborish',
    'lokatsiyalarni boshqarish'  # New command for location management
])
def handle_admin_actions(message):
    handle_admin_commands(message)

# Ro'yxatdan o'tish jarayonini boshqarish
@bot.message_handler(func=lambda message: True)
def handle_registration(message):
    handle_registration_steps(message)

# Botni ishga tushirish
if __name__ == '__main__':
    bot.polling(none_stop=True)
