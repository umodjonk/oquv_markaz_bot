import os
import psycopg2
import logging
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

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def fetch_courses():
    """Fetches all courses from the PostgreSQL database."""
    query = "SELECT * FROM courses"
    return execute_query(query)

def fetch_course_by_id(course_id):
    """Fetches a course by its ID."""
    query = "SELECT * FROM courses WHERE course_id = %s"
    results = execute_query(query, (course_id,))
    return results[0] if results else None

def fetch_course_by_name(name):
    """Fetches a course by its name."""
    query = "SELECT * FROM courses WHERE name ILIKE %s"
    results = execute_query(query, (name,))
    return results[0] if results else None

def search_courses(query):
    """Searches for courses by name matching the query."""
    sql_query = "SELECT * FROM courses WHERE name ILIKE %s"
    params = (f"%{query}%",)
    return execute_query(sql_query, params)

def fetch_users():
    """Fetches all users from the database."""
    query = "SELECT id, name, surname FROM users"
    results = execute_query(query)
    if not results:
        logging.info("No users found.")
    return results

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

def create_tables():
    """Creates the necessary tables."""
    queries = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT,
            surname TEXT,
            dob DATE,
            phone TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS courses (
            course_id SERIAL PRIMARY KEY,
            name TEXT UNIQUE,
            price REAL,
            description TEXT,
            instructor TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS advertisements (
            ad_id SERIAL PRIMARY KEY,
            ad_text TEXT UNIQUE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS locations (
            location_id SERIAL PRIMARY KEY,
            name TEXT,
            address TEXT,
            latitude REAL,
            longitude REAL
        )
        """
    ]
    for query in queries:
        execute_query(query)
    logging.info("Tables created successfully.")

def seed_data():
    """Seeds the courses table with initial data."""
    query = """
    INSERT INTO courses (name, price, description, instructor)
    VALUES
    ('Frontend Development', 100, 'Basic Frontend Development Course', 'John Doe'),
    ('Backend Development', 150, 'Advanced Backend Development Course', 'Jane Smith')
    ON CONFLICT (name) DO NOTHING
    """
    execute_query(query)
    logging.info("Seed data inserted successfully.")

def add_advertisement(ad_text):
    """Adds a new advertisement to the database."""
    query = """
    INSERT INTO advertisements (ad_text)
    VALUES (%s)
    ON CONFLICT (ad_text) DO NOTHING
    """
    execute_query(query, (ad_text,))

def add_location(name, address, latitude, longitude):
    """Adds a new location to the database."""
    query = """
    INSERT INTO locations (name, address, latitude, longitude)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (name, address) DO NOTHING
    """
    execute_query(query, (name, address, latitude, longitude))

def fetch_locations():
    """Fetches all locations from the database."""
    query = "SELECT * FROM locations"
    return execute_query(query)

def fetch_location_by_id(location_id):
    """Fetches a location by its ID."""
    query = "SELECT * FROM locations WHERE location_id = %s"
    results = execute_query(query, (location_id,))
    return results[0] if results else None

def fetch_location_by_name(name):
    """Fetches a location by its name."""
    query = "SELECT * FROM locations WHERE name ILIKE %s"
    results = execute_query(query, (name,))
    return results[0] if results else None

def update_location(location_id, name, address, latitude, longitude):
    """Updates an existing location in the database."""
    query = """
    UPDATE locations
    SET name = %s, address = %s, latitude = %s, longitude = %s
    WHERE location_id = %s
    """
    execute_query(query, (name, address, latitude, longitude, location_id))

def delete_location(location_id):
    """Deletes a location from the database."""
    query = "DELETE FROM locations WHERE location_id = %s"
    execute_query(query, (location_id,))
