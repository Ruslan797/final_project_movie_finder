client = MongoClient(
    "mongodb://ich_editor:verystrongpassword@mongo.itcareerhub.de/?readPreference=primary&ssl=false&authMechanism=DEFAULT&authSource=ich_edit"
)

import pymysql

def get_connection():
    config = {
        "host": "ich-db.edu.itcareerhub.de",
        "user": "ich1",
        "password": "password",
        "database": "sakila"
    }
    return pymysql.connect(**config)

def search_by_keyword(keyword, offset=0, limit=10):
    query = f"""
        SELECT title
        FROM film
        WHERE title LIKE %s
        LIMIT %s OFFSET %s
    """
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(query, (f"%{keyword}%", limit, offset))
        return cursor.fetchall()

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

