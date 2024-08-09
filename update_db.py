import sqlite3


def update_user_profile(user_id, name=None, surname=None, dob=None, phone=None):
    """Update user profile information in the database."""
    conn = sqlite3.connect('bot_database.db')  # Adjust the database connection as needed
    cursor = conn.cursor()

    # Build the update query dynamically
    fields = []
    params = []

    if name:
        fields.append("name = ?")
        params.append(name)
    if surname:
        fields.append("surname = ?")
        params.append(surname)
    if dob:
        fields.append("dob = ?")
        params.append(dob)
    if phone:
        fields.append("phone = ?")
        params.append(phone)

    if not fields:
        print("No fields to update.")
        conn.close()
        return  # No fields to update

    set_clause = ", ".join(fields)
    params.append(user_id)

    query = f"UPDATE users SET {set_clause} WHERE user_id = ?"

    try:
        cursor.execute(query, params)
        conn.commit()
        print("User profile updated successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def update_table_structure():
    """Update the database schema to ensure it has the necessary columns."""
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()

    try:
        # Check if 'course_id' column already exists
        cursor.execute("PRAGMA table_info(courses);")
        columns = [row[1] for row in cursor.fetchall()]

        if 'course_id' not in columns:
            # Add the 'course_id' column if it doesn't exist
            cursor.execute("ALTER TABLE courses ADD COLUMN course_id INTEGER PRIMARY KEY AUTOINCREMENT;")
            conn.commit()
            print("Column 'course_id' added to 'courses' table.")
        else:
            print("Column 'course_id' already exists in 'courses' table.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    update_user_profile(user_id=1, name="John", surname="Doe", dob="2000-01-01", phone="1234567890")
    update_table_structure()
