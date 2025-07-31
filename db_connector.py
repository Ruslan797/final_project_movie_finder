import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Ошибка подключения к MySQL: {e}")
    return None

def search_by_keyword(keyword, offset=0, limit=10):
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        query = "SELECT title FROM movies WHERE title LIKE %s LIMIT %s OFFSET %s"
        cursor.execute(query, (f"%{keyword}%", limit, offset))
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Ошибка запроса: {e}")
        return []
    finally:
        if conn.is_connected():
            conn.close()


def get_genres():
    query = "SELECT name FROM category"
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]

def get_year_range():
    query = "SELECT MIN(release_year), MAX(release_year) FROM film"
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()

def search_by_genre_and_year(genre, start_year, end_year, offset=0, limit=10):
    query = """
        SELECT film.title, release_year
        FROM film
        JOIN film_category ON film.film_id = film_category.film_id
        JOIN category ON category.category_id = film_category.category_id
        WHERE category.name = %s AND release_year BETWEEN %s AND %s
        LIMIT %s OFFSET %s
    """
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(query, (genre, start_year, end_year, limit, offset))
        return cursor.fetchall()

