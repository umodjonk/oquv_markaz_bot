import telebot
from telebot import types
from db import add_course, delete_course, fetch_courses, fetch_users

user_state = {}

def admin_panel_handler(bot, message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    add_course_button = types.KeyboardButton("Kurs qo'shish")
    remove_course_button = types.KeyboardButton("Kurs o'chirish")
    view_users_button = types.KeyboardButton("Foydalanuvchilarni ko'rish")
    send_ad_button = types.KeyboardButton("Reklama yuborish")
    markup.add(add_course_button, remove_course_button, view_users_button, send_ad_button)
    bot.send_message(user_id, "Admin panel", reply_markup=markup)

def handle_admin_commands(bot, message):
    user_id = message.from_user.id
    command = message.text.lower()

    if command == 'kurs qo\'shish':
        user_state[user_id] = {'step': 'add_course_name'}
        bot.send_message(user_id, "Kurs qo'shish uchun kerakli ma'lumotlarni yuboring.")
    elif command == 'kurs o\'chirish':
        user_state[user_id] = {'step': 'delete_course'}
        bot.send_message(user_id, "O'chiriladigan kurs nomini yuboring.")
    elif command == 'foydalanuvchilarni ko\'rish':
        users = fetch_users()
        if users:
            users_list = '\n'.join([f"ID: {user[0]}, Ism: {user[1]}, Familya: {user[2]}" for user in users])
            bot.send_message(user_id, f"Foydalanuvchilar:\n{users_list}")
        else:
            bot.send_message(user_id, "Hech qanday foydalanuvchi topilmadi.")
    elif command == 'reklama yuborish':
        user_state[user_id] = {'step': 'send_ad'}
        bot.send_message(user_id, "Reklama matnini yuboring.")

def handle_admin_steps(bot, message):
    """Handles the step-by-step processes for admin tasks."""
    user_id = message.from_user.id
    step = user_state.get(user_id, {}).get('step')

    if step == 'add_course_name':
        user_state[user_id]['course_name'] = message.text
        bot.send_message(user_id, "Kurs narxini kiriting:")
        user_state[user_id]['step'] = 'add_course_price'
    elif step == 'add_course_price':
        user_state[user_id]['course_price'] = message.text
        bot.send_message(user_id, "Kurs tavsifini kiriting:")
        user_state[user_id]['step'] = 'add_course_description'
    elif step == 'add_course_description':
        user_state[user_id]['course_description'] = message.text
        bot.send_message(user_id, "Kurs muallifini kiriting:")
        user_state[user_id]['step'] = 'add_course_instructor'
    elif step == 'add_course_instructor':
        course_data = user_state[user_id]
        add_course(course_data['course_name'], course_data['course_price'], course_data['course_description'],
                   course_data['course_instructor'])
        bot.send_message(user_id, "Kurs qo'shildi!")
        user_state[user_id] = {'step': None}
    elif step == 'delete_course':
        course_name = message.text
        # Fetch course by name to get its ID
        courses = fetch_courses()
        course = next((c for c in courses if c[1].lower() == course_name.lower()), None)
        if course:
            course_id = course[0]
            delete_course(course_id)
            bot.send_message(user_id, f"{course_name} kursi o'chirildi.")
        else:
            bot.send_message(user_id, "Kurs topilmadi.")
        user_state[user_id] = {'step': None}
    elif step == 'send_ad':
        ad_text = message.text
        # Example code to send ad to all users
        users = fetch_users()
        for user in users:
            user_id = user[0]
            bot.send_message(user_id, ad_text)
        bot.send_message(user_id, "Reklama yuborildi!")
        user_state[user_id] = {'step': None}

def setup_admin_handlers(bot):
    """Sets up handlers for admin commands."""
    bot.message_handler(commands=['admin'])(admin_panel_handler)
    bot.message_handler(
        func=lambda message: message.text.lower() in ["kurs qo'shish", "kurs o'chirish", "foydalanuvchilarni ko'rish",
                                                      "reklama yuborish"])(handle_admin_commands)
    bot.message_handler(func=lambda message: user_state.get(message.from_user.id, {}).get('step') is not None)(
        handle_admin_steps)

# Usage example:
# bot = telebot.TeleBot("YOUR_BOT_TOKEN")
# setup_admin_handlers(bot)
# bot.polling()
