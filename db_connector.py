import pymysql
from .config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def get_connection():
    """
    Устанавливает соединение с MySQL-базой данных.
    Возвращает объект подключения или None при ошибке.
    """
    try:
        return pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        print(f"Ошибка подключения к MySQL: {e}")
        return None

def get_genres():
    """
    Получает все жанры (категории фильмов) из таблицы category.
    Возвращает список словарей с ключами category_id и name.
    """
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT category_id, name FROM category ORDER BY name;")
            return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка получения жанров: {e}")
        return []
    finally:
        conn.close()

def get_year_range():
    """
    Получает минимальный и максимальный год выпуска фильмов.
    Используется для ограничения диапазона поиска по годам.
    Возвращает словарь с min_year и max_year.
    """
    conn = get_connection()
    if not conn:
        return {"min_year": None, "max_year": None}
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT MIN(release_year) as min_year, MAX(release_year) as max_year FROM film;")
            return cursor.fetchone()
    except Exception as e:
        print(f"Ошибка получения диапазона лет: {e}")
        return {"min_year": None, "max_year": None}
    finally:
        conn.close()

def search_by_keyword(keyword, offset=0, limit=10):
    """
    Поиск фильмов по ключевому слову в названии.
    Параметры:
        keyword (str) — строка для поиска
        offset (int) — смещение для пагинации
        limit (int) — количество результатов на страницу
    Возвращает список фильмов.
    """
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT film_id, title, release_year, description
                FROM film
                WHERE title LIKE %s
                ORDER BY title
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (f'%{keyword}%', limit, offset))
            return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка поиска по ключевому слову: {e}")
        return []
    finally:
        conn.close()

def search_by_genre_and_year(genre_id, year_from, year_to, offset=0, limit=10):
    """
    Поиск фильмов по жанру и диапазону лет.
    Параметры:
        genre_id (int) — id жанра
        year_from (int) — начальный год
        year_to (int) — конечный год
        offset (int) — смещение для пагинации
        limit (int) — количество результатов на страницу
    Возвращает список фильмов.
    """
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT f.film_id, f.title, f.release_year, f.description
                FROM film f
                JOIN film_category fc ON f.film_id = fc.film_id
                WHERE fc.category_id = %s AND f.release_year BETWEEN %s AND %s
                ORDER BY f.title
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (genre_id, year_from, year_to, limit, offset))
            return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка поиска по жанру и году: {e}")
        return []
    finally:
        conn.close()