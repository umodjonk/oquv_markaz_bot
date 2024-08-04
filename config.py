import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# Telegram bot tokenini olish
TOKEN = os.getenv('BOT_TOKEN', 'YOUR_DEFAULT_BOT_TOKEN')
if TOKEN == 'YOUR_DEFAULT_BOT_TOKEN':
    raise ValueError("Bot token is not defined in .env file.")

# Til sozlamalari
LANGUAGE = {
    'uz': {
        'start_message': "Salom! Iltimos, tilni tanlang.",
        'welcome_message': "Siz tilni tanladingiz, kurslarimizdan birini tanlang.",
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
        'register_name': "Пожалуйста, введите ваше имя.",
        'register_surname': "Пожалуйста, введите вашу фамилию.",
        'register_dob': "Пожалуйста, введите вашу дату рождения (YYYY-MM-DD).",
        'register_phone': "Пожалуйста, введите ваш телефонный номер."
    }
}