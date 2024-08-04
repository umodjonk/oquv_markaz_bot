import telebot
from database import fetch_courses, add_course, delete_course, fetch_users, add_advertisement, fetch_locations, add_location, delete_location

def admin_panel_handler(message):
    """Handles the admin panel command and provides options to the admin."""
    # Assuming you're using an admin check function, implement it accordingly
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "Siz ushbu panelga kirishga ruxsat etilmasiz.")
        return

    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    markup.add("Kurs qo'shish", "Kurs o'chirish", "Foydalanuvchilarni ko'rish", "Reklama yuborish", "Locatsiyalarni boshqarish")
    bot.send_message(message.chat.id, "Admin panelga xush kelibsiz! Quyidagi variantlardan birini tanlang:",
                     reply_markup=markup)

def handle_admin_commands(message):
    """Handles admin commands based on the user's input."""
    command = message.text.lower()

    if command == "kurs qo'shish":
        prompt_for_course_details(message)
    elif command == "kurs o'chirish":
        prompt_for_course_deletion(message)
    elif command == "foydalanuvchilarni ko'rish":
        display_users(message)
    elif command == "reklama yuborish":
        prompt_for_advertisement(message)
    elif command == "locatsiyalarni boshqarish":
        manage_locations(message)

def prompt_for_course_details(message):
    """Prompts the admin to provide course details."""
    bot.send_message(message.chat.id, "Iltimos, yangi kurs uchun nomni kiriting:")
    bot.register_next_step_handler(message, process_course_name)

def process_course_name(message):
    """Processes the course name and asks for additional details."""
    course_name = message.text
    bot.send_message(message.chat.id, "Kursning narxini kiriting:")
    bot.register_next_step_handler(message, process_course_price, course_name)

def process_course_price(message, course_name):
    """Processes the course price and asks for the description."""
    try:
        course_price = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Narx raqam bo'lishi kerak. Iltimos, qaytadan kiriting:")
        bot.register_next_step_handler(message, process_course_price, course_name)
        return

    bot.send_message(message.chat.id, "Kursning tavsifini kiriting:")
    bot.register_next_step_handler(message, process_course_description, course_name, course_price)

def process_course_description(message, course_name, course_price):
    """Processes the course description and asks for the instructor."""
    course_description = message.text
    bot.send_message(message.chat.id, "Kursning o'qituvchisini kiriting:")
    bot.register_next_step_handler(message, finalize_course_addition, course_name, course_price, course_description)

def finalize_course_addition(message, course_name, course_price, course_description):
    """Adds the course to the database."""
    course_instructor = message.text
    add_course(course_name, course_price, course_description, course_instructor)
    bot.send_message(message.chat.id, "Kurs muvaffaqiyatli qo'shildi.")

def prompt_for_course_deletion(message):
    """Prompts the admin to provide the course ID for deletion."""
    bot.send_message(message.chat.id, "O'chirish uchun kurs ID'sini kiriting:")
    bot.register_next_step_handler(message, process_course_deletion)

def process_course_deletion(message):
    """Deletes the course from the database."""
    try:
        course_id = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "ID raqam bo'lishi kerak. Iltimos, qaytadan kiriting:")
        bot.register_next_step_handler(message, process_course_deletion)
        return

    delete_course(course_id)
    bot.send_message(message.chat.id, "Kurs muvaffaqiyatli o'chirildi.")

def display_users(message):
    """Displays the list of users."""
    users = fetch_users()
    if not users:
        bot.send_message(message.chat.id, "Hech qanday foydalanuvchi topilmadi.")
        return

    user_list = "\n".join([f"{user[1]} {user[2]}" for user in users])
    bot.send_message(message.chat.id, f"Foydalanuvchilar ro'yxati:\n{user_list}")

def prompt_for_advertisement(message):
    """Prompts the admin to provide advertisement text."""
    bot.send_message(message.chat.id, "Reklama matnini kiriting:")
    bot.register_next_step_handler(message, process_advertisement)

def process_advertisement(message):
    """Adds the advertisement to the database."""
    ad_text = message.text
    add_advertisement(ad_text)
    bot.send_message(message.chat.id, "Reklama muvaffaqiyatli yuborildi.")

def manage_locations(message):
    """Manages locations by providing options to the admin."""
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    markup.add("Locatsiya qo'shish", "Locatsiya o'chirish", "Locatsiyalarni ko'rish")
    bot.send_message(message.chat.id, "Locatsiyalarni boshqarish bo'limi. Quyidagi variantlardan birini tanlang:",
                     reply_markup=markup)

def handle_location_commands(message):
    """Handles location commands based on the user's input."""
    command = message.text.lower()

    if command == "locatsiya qo'shish":
        prompt_for_location_details(message)
    elif command == "locatsiya o'chirish":
        prompt_for_location_deletion(message)
    elif command == "locatsiyalarni ko'rish":
        display_locations(message)

def prompt_for_location_details(message):
    """Prompts the admin to provide location details."""
    bot.send_message(message.chat.id, "Iltimos, yangi locatsiya nomini kiriting:")
    bot.register_next_step_handler(message, process_location_name)

def process_location_name(message):
    """Processes the location name and asks for additional details."""
    location_name = message.text
    bot.send_message(message.chat.id, "Locatsiyaning manzilini kiriting:")
    bot.register_next_step_handler(message, finalize_location_addition, location_name)

def finalize_location_addition(message, location_name):
    """Adds the location to the database."""
    location_address = message.text
    add_location(location_name, location_address)
    bot.send_message(message.chat.id, "Locatsiya muvaffaqiyatli qo'shildi.")

def prompt_for_location_deletion(message):
    """Prompts the admin to provide the location ID for deletion."""
    bot.send_message(message.chat.id, "O'chirish uchun locatsiya ID'sini kiriting:")
    bot.register_next_step_handler(message, process_location_deletion)

def process_location_deletion(message):
    """Deletes the location from the database."""
    try:
        location_id = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "ID raqam bo'lishi kerak. Iltimos, qaytadan kiriting:")
        bot.register_next_step_handler(message, process_location_deletion)
        return

    delete_location(location_id)
    bot.send_message(message.chat.id, "Locatsiya muvaffaqiyatli o'chirildi.")

def display_locations(message):
    """Displays the list of locations."""
    locations = fetch_locations()
    if not locations:
        bot.send_message(message.chat.id, "Hech qanday locatsiya topilmadi.")
        return

    location_list = "\n".join([f"{location[1]}: {location[2]}" for location in locations])
    bot.send_message(message.chat.id, f"Locatsiyalar ro'yxati:\n{location_list}")

def is_admin(user_id):
    """Check if the user is an admin. Implement this function based on your admin verification."""
    # Example check (replace with your actual admin ID or logic)
    return user_id == YOUR_ADMIN_ID

# Ensure the bot instance is available here if used elsewhere
# bot = telebot.TeleBot(TOKEN)
