from telebot import types
from db import fetch_courses, fetch_course_by_name, add_user, search_courses, add_course, delete_course, add_advertisement
from config import LANGUAGE, TOKEN
import telebot

user_state = {}

# Admin ID
ADMIN_ID = 6893899631  # Replace with your Admin's Telegram ID

bot = telebot.TeleBot(TOKEN)

def start_handler(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    uz_button = types.KeyboardButton("O'zbekcha")
    ru_button = types.KeyboardButton("Русский")
    markup.add(uz_button, ru_button)

    if user_id == ADMIN_ID:
        admin_button = types.KeyboardButton("Admin Panel")
        markup.add(admin_button)

    bot.send_message(user_id, LANGUAGE['uz']['start_message'], reply_markup=markup)

def handle_start(message):
    start_handler(message)

def language_selection_handler(message):
    user_id = message.from_user.id
    language = 'uz' if message.text.lower() == "o'zbekcha" else 'ru'
    user_state[user_id] = {'language': language, 'step': None}

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    courses_button = types.KeyboardButton(LANGUAGE[language]['courses_button'])
    about_button = types.KeyboardButton(LANGUAGE[language]['about_button'])
    location_button = types.KeyboardButton(LANGUAGE[language]['location_button'])
    contact_button = types.KeyboardButton(LANGUAGE[language]['contact_button'])
    markup.add(courses_button, about_button, location_button, contact_button)

    if user_id == ADMIN_ID:
        admin_button = types.KeyboardButton("Admin Panel")
        markup.add(admin_button)

    bot.send_message(user_id, LANGUAGE[language]['welcome_message'], reply_markup=markup)

def registration_handler(message):
    user_id = message.from_user.id
    if user_id not in user_state:
        user_state[user_id] = {'step': 'initial', 'language': 'uz'}  # Default language
    user_state[user_id]['step'] = 'name'
    language = user_state[user_id].get('language', 'uz')
    bot.send_message(user_id, LANGUAGE[language]['register_name'])

def handle_registration_steps(message):
    user_id = message.from_user.id
    language = user_state.get(user_id, {}).get('language', 'uz')
    step = user_state.get(user_id, {}).get('step')

    if step == 'name':
        user_state[user_id]['name'] = message.text
        user_state[user_id]['step'] = 'surname'
        bot.send_message(user_id, LANGUAGE[language]['register_surname'])
    elif step == 'surname':
        user_state[user_id]['surname'] = message.text
        user_state[user_id]['step'] = 'dob'
        bot.send_message(user_id, LANGUAGE[language]['register_dob'])
    elif step == 'dob':
        user_state[user_id]['dob'] = message.text
        user_state[user_id]['step'] = 'phone'
        bot.send_message(user_id, LANGUAGE[language]['register_phone'])
    elif step == 'phone':
        user_state[user_id]['phone'] = message.text
        user_data = user_state[user_id]
        add_user(user_id, user_data['name'], user_data['surname'], user_data['dob'], user_data['phone'])
        bot.send_message(user_id, (f"Ro'yxatdan o'tdingiz!\n"
                                   f"Ism: {user_data['name']}\n"
                                   f"Familya: {user_data['surname']}\n"
                                   f"Tug'ilgan kun: {user_data['dob']}\n"
                                   f"Telefon: {user_data['phone']}"))
        user_state[user_id]['step'] = None
        show_courses(message)

def show_courses(message):
    user_id = message.from_user.id
    courses = fetch_courses()

    if not courses:
        bot.send_message(user_id, "Kurslar topilmadi.")
        return

    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for course in courses:
        course_id, name, price, description, instructor = course
        button = types.KeyboardButton(text=name)
        markup.add(button)

    bot.send_message(user_id, "Kursni tanlang:", reply_markup=markup)

def handle_course_selection(message):
    user_id = message.from_user.id
    course_name = message.text
    course = fetch_course_by_name(course_name)

    if course:
        course_id, name, price, description, instructor = course
        course_message = (f"Kurs: {name}\n"
                          f"Narx: {price}\n"
                          f"Tavsif: {description}\n"
                          f"Muallif: {instructor}")
        bot.send_message(user_id, course_message)
    else:
        bot.send_message(user_id, "Kurs topilmadi.")

def handle_course_search(message):
    search_term = message.text[len('kurs qidirish:'):].strip()
    courses = search_courses(search_term)

    if courses:
        courses_list = '\n'.join(
            [f"ID: {course[0]}, Kurs: {course[1]}, Narx: {course[2]}, Tavsif: {course[3]}, Muallif: {course[4]}" for
             course in courses])
        bot.send_message(message.from_user.id, f"Topilgan kurslar:\n{courses_list}")
    else:
        bot.send_message(message.from_user.id, "Kurslar topilmadi.")

def admin_panel_handler(message):
    """Admin panelni ko'rsatadi."""
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add('Kurs qo\'shish', 'Kurs o\'chirish', 'Foydalanuvchilarni ko\'rish', 'Reklama yuborish')
    bot.send_message(message.chat.id, "Admin panel:", reply_markup=keyboard)

def handle_admin_panel_actions(message):
    if message.from_user.id == ADMIN_ID:
        if message.text == "Kurs qo'shish":
            bot.send_message(message.from_user.id, "Kurs qo'shish uchun nom, narx, tavsif va muallifni yuboring.")
            user_state[message.from_user.id]['step'] = 'add_course'
        elif message.text == "Kurs o'chirish":
            courses = fetch_courses()
            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            for course in courses:
                button = types.KeyboardButton(text=course[1])  # Kurs nomi
                markup.add(button)
            bot.send_message(message.from_user.id, "O'chirish uchun kursni tanlang:", reply_markup=markup)
            user_state[message.from_user.id]['step'] = 'delete_course'
        elif message.text == "Reklama yuborish":
            bot.send_message(message.from_user.id, "Reklama matnini yuboring.")
            user_state[message.from_user.id]['step'] = 'add_advertisement'

def handle_admin_actions(message):
    user_id = message.from_user.id
    step = user_state.get(user_id, {}).get('step')
    if step == 'add_course':
        course_details = message.text.split('\n')
        if len(course_details) == 4:
            name = course_details[0]
            price = course_details[1]
            description = course_details[2]
            instructor = course_details[3]
            add_course(name, price, description, instructor)
            bot.send_message(user_id, f"Kurs qo'shildi: {name}")
        else:
            bot.send_message(user_id, "Noto'g'ri ma'lumotlar. Iltimos, to'g'ri formatda yuboring.")
    elif step == 'delete_course':
        course_name = message.text
        delete_course(course_name)
        bot.send_message(user_id, f"Kurs o'chirildi: {course_name}")
    elif step == 'add_advertisement':
        advertisement_text = message.text
        add_advertisement(advertisement_text)
        bot.send_message(user_id, "Reklama yuborildi.")

def handle_location(message):
    user_id = message.from_user.id
    regions = {
        'Toshkent': ['Yunusobod', 'Mirobod', 'Chilonzor'],
        'Samarqand': ['Samarqand', 'Keshkent', 'Jomboy'],
        'Buxoro': ['Buxoro', 'Qorakoʻl', 'Vobkent']
    }

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for region in regions.keys():
        button = types.KeyboardButton(text=region)
        markup.add(button)
    bot.send_message(user_id, "Viloyatni tanlang:", reply_markup=markup)
    user_state[user_id]['step'] = 'region'

def location_content_handler(message):
    user_id = message.from_user.id
    region = message.text
    regions = {
        'Toshkent': ['Yunusobod', 'Mirobod', 'Chilonzor'],
        'Samarqand': ['Samarqand', 'Keshkent', 'Jomboy'],
        'Buxoro': ['Buxoro', 'Qorakoʻl', 'Vobkent']
    }

    if region in regions:
        districts = regions[region]
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        for district in districts:
            button = types.KeyboardButton(text=district)
            markup.add(button)
        bot.send_message(user_id, "Tumanlarni tanlang:", reply_markup=markup)
    else:
        bot.send_message(user_id, "Viloyat topilmadi.")

def handle_contact(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Aloqa uchun quyidagi kanalda bizni topishingiz mumkin: [Link to Channel]")

@bot.message_handler(commands=['start'])
def start(message):
    handle_start(message)

@bot.message_handler(func=lambda message: message.text.lower() in ['o\'zbekcha', 'русский'])
def handle_language(message):
    language_selection_handler(message)

@bot.message_handler(func=lambda message: message.text.lower() == 'kurslarimiz')
def registration(message):
    registration_handler(message)

@bot.message_handler(func=lambda message: message.text.startswith('kurs qidirish:'))
def search_courses_handler(message):
    handle_course_search(message)

@bot.message_handler(func=lambda message: message.text.lower() in ['biz haqimizda', 'о нас'])
def about(message):
    bot.send_message(message.from_user.id, "Biz haqimizda ma'lumot.")

@bot.message_handler(func=lambda message: message.text.lower() in ['locatsiya', 'местоположение'])
def location(message):
    handle_location(message)

@bot.message_handler(func=lambda message: message.text.lower() in ['aloqa', 'контакт'])
def contact(message):
    handle_contact(message)

@bot.message_handler(func=lambda message: message.text.lower() in ['admin panel'])
def admin_panel(message):
    admin_panel_handler(message)

@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID, content_types=['text'])
def handle_admin(message):
    handle_admin_panel_actions(message)

@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID)
def admin_actions(message):
    handle_admin_actions(message)

@bot.message_handler(func=lambda message: message.text in [course[1] for course in fetch_courses()])
def handle_course(message):
    handle_course_selection(message)

@bot.message_handler(func=lambda message: message.text in ['Toshkent', 'Samarqand', 'Buxoro'])
def handle_region(message):
    location_content_handler(message)

@bot.message_handler(func=lambda message: message.text in ['Yunusobod', 'Mirobod', 'Chilonzor', 'Samarqand', 'Keshkent', 'Jomboy', 'Buxoro', 'Qorakoʻl', 'Vobkent'])
def handle_district(message):
    bot.send_message(message.from_user.id, f"Tuman: {message.text}")

# Start polling
bot.polling(none_stop=True)
