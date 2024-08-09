import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# Telegram bot tokenini olish
TOKEN = os.getenv('BOT_TOKEN', 'YOUR_DEFAULT_BOT_TOKEN')
if TOKEN == 'YOUR_DEFAULT_BOT_TOKEN':
    raise ValueError("Bot token is not defined in .env file.")
# Channel ID where users need to subscribe
CHANNEL_ID = 'https://t.me/shahzodtelegramappstore'  # Or use the numeric ID, e.g., -1001234567890
LANGUAGE = {
    'uz': {
        'start_message': "Salom! Iltimos, tilni tanlang.",
        'welcome_message': "Siz tilni tanladingiz. Kurslarimizdan birini tanlang.",
        'courses_button': "Kurslarimiz",
        'about_button': "Biz haqimizda",
        'location_button': "Locatsiya",
        'contact_button': "Aloqa",
        'register_name': "Ismingizni kiriting.",
        'register_surname': "Familyangizni kiriting.",
        'register_dob': "Tug'ilgan kuningizni kiriting (YYYY-MM-DD).",
        'register_phone': "Telefon raqamingizni kiriting."
    },
    'ru': {
        'start_message': "Здравствуйте! Пожалуйста, выберите язык.",
        'welcome_message': "Вы выбрали русский язык. Пожалуйста, выберите из меню.",
        'courses_button': "Наши курсы",
        'about_button': "О нас",
        'location_button': "Местоположение",
        'contact_button': "Контакт",
        'register_name': "Введите ваше имя.",
        'register_surname': "Введите вашу фамилию.",
        'register_dob': "Введите вашу дату рождения (YYYY-MM-DD).",
        'register_phone': "Введите ваш телефонный номер."
    }
}
