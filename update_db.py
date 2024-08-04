import sqlite3

def update_table_structure():
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()

    try:
        # Agar 'course_id' ustuni mavjud bo'lmasa, qo'shish
        cursor.execute("ALTER TABLE courses ADD COLUMN course_id INTEGER PRIMARY KEY AUTOINCREMENT")
        conn.commit()
    except sqlite3.OperationalError:
        # 'course_id' ustuni allaqachon mavjud bo'lsa, hech narsa qilmaydi
        pass

    conn.close()

if __name__ == "__main__":
    update_table_structure()
