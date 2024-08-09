from telebot import types
from db import fetch_courses, fetch_course_by_name, add_user
from config import LANGUAGE, TOKEN
import telebot

user_state = {}

bot = telebot.TeleBot(TOKEN)

# Admin ID
ADMIN_ID = 6893899631  # Replace with your Admin's Telegram ID


def start_handler(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    uz_button = types.KeyboardButton("O'zbekcha")
    ru_button = types.KeyboardButton("Русский")
    markup.add(uz_button, ru_button)

    bot.send_message(user_id, LANGUAGE['uz']['start_message'], reply_markup=markup)


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

    bot.send_message(user_id, LANGUAGE[language]['welcome_message'], reply_markup=markup)


def registration_handler(message):
    user_id = message.from_user.id
    user_state[user_id] = {'step': 'name', 'language': user_state.get(user_id, {}).get('language', 'uz')}
    language = user_state[user_id]['language']
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
        user_state[user_id]['step'] = None
        show_courses(message)


def show_courses(message):
    user_id = message.from_user.id
    courses = fetch_courses()

    if not courses:
        bot.send_message(user_id, "Kurslar topilmadi.")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)

    for course in courses:
        course_id, name, price, description, instructor = course
        button = types.InlineKeyboardButton(text=name, callback_data=f'course_{course_id}')
        markup.add(button)

    bot.send_message(user_id, "Kursni tanlang:", reply_markup=markup)


def handle_course_selection(call):
    course_id = call.data.split('_')[1]
    course = fetch_course_by_name(course_id)

    if course:
        course_id, name, price, description, instructor = course
        course_message = (f"Kurs: {name}\n"
                          f"Narx: {price}\n"
                          f"Tavsif: {description}\n"
                          f"Muallif: {instructor}")
        bot.send_message(call.from_user.id, course_message)
    else:
        bot.send_message(call.from_user.id, "Kurs topilmadi.")


@bot.message_handler(commands=['start'])
def handle_start_command(message):
    start_handler(message)


@bot.message_handler(func=lambda message: message.text in ["O'zbekcha", "Русский"])
def handle_language_selection(message):
    language_selection_handler(message)


@bot.message_handler(func=lambda message: message.text == 'Kurslarimiz')
def handle_courses(message):
    registration_handler(message)


@bot.message_handler(
    func=lambda message: user_state.get(message.from_user.id, {}).get('step') in ['name', 'surname', 'dob', 'phone'])
def handle_registration(message):
    handle_registration_steps(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('course_'))
def handle_course_selection_call(call):
    handle_course_selection(call)


bot.polling(none_stop=True)
