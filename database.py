import psycopg2
import logging
import os
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path, encoding='utf-8')

# Database connection parameters
DATABASE = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 5432))  # Default to 5432 if not set
}

def connect_db():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=DATABASE['dbname'],
            user=DATABASE['user'],
            password=DATABASE['password'],
            host=DATABASE['host'],
            port=DATABASE['port']
        )
        logging.info("Database connection successful.")
        return conn
    except psycopg2.Error as e:
        logging.error(f"Database connection error: {e}")
        return None
    except UnicodeDecodeError as e:
        logging.error(f"Unicode decode error: {e}")
        return None

def execute_query(query, params=()):
    """Executes an SQL query and returns the results."""
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if query.strip().upper().startswith("SELECT"):
                    results = cursor.fetchall()
                else:
                    results = None
                    conn.commit()  # Commit changes for non-SELECT queries
            return results
        except psycopg2.Error as e:
            logging.error(f"Error executing query: {e}")
            return None
        finally:
            conn.close()
    return None

# Courses Functions
def fetch_courses():
    """Fetches all courses from the PostgreSQL database."""
    query = "SELECT * FROM courses"
    return execute_query(query)

def add_course(name, price, description, instructor):
    """Adds a new course to the database."""
    query = """
    INSERT INTO courses (name, price, description, instructor)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (name) DO NOTHING
    """
    execute_query(query, (name, price, description, instructor))

def delete_course(course_id):
    """Deletes a course from the database."""
    query = "DELETE FROM courses WHERE course_id = %s"
    execute_query(query, (course_id,))

# Users Functions
def fetch_users():
    """Fetches all users from the database."""
    query = "SELECT id, name, surname FROM users"
    results = execute_query(query)
    if not results:
        logging.info("No users found.")
    return results

def add_user(user_id, name, surname, dob, phone):
    """Adds or updates a user in the database."""
    query = """
    INSERT INTO users (id, name, surname, dob, phone)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (id) DO UPDATE
    SET name = EXCLUDED.name,
        surname = EXCLUDED.surname,
        dob = EXCLUDED.dob,
        phone = EXCLUDED.phone
    """
    execute_query(query, (user_id, name, surname, dob, phone))

def get_user(user_id):
    """Returns user data."""
    query = "SELECT * FROM users WHERE id = %s"
    return execute_query(query, (user_id,)) or [None]

def is_user_registered(user_id):
    """Checks if a user is registered."""
    query = "SELECT 1 FROM users WHERE id = %s"
    return execute_query(query, (user_id,)) is not None

# Advertisements Functions
def add_advertisement(ad_text):
    """Adds a new advertisement to the database."""
    query = """
    INSERT INTO advertisements (ad_text)
    VALUES (%s)
    ON CONFLICT (ad_text) DO NOTHING
    """
    execute_query(query, (ad_text,))

# Locations Functions
def add_location(name, address, latitude, longitude):
    """Adds a new location to the database."""
    query = """
    INSERT INTO locations (name, address, latitude, longitude)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (name) DO NOTHING
    """
    execute_query(query, (name, address, latitude, longitude))

def fetch_locations():
    """Fetches all locations from the database."""
    query = "SELECT * FROM locations"
    return execute_query(query)
def fetch_location_by_name(name):
    """Fetches a location by its name."""
    query = "SELECT * FROM locations WHERE name ILIKE %s"
    results = execute_query(query, (name,))
    return results[0] if results else None

def delete_location(location_id):
    """Deletes a location from the database."""
    query = "DELETE FROM locations WHERE id = %s"
    execute_query(query, (location_id,))
