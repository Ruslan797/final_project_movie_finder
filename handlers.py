from input_validator import validate_genre, validate_years, validate_keyword
from db_connector import search_by_genre_and_year, search_by_keyword
from formatter import format_table

def handle_genre_year_search():
    genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi']
    print("\nДоступные жанры:", ", ".join(genres))
    genre = input("Выберите жанр: ")
    if not validate_genre(genre, genres):
        return

    try:
        start_year = int(input("С какого года: "))
        end_year = int(input("До какого года: "))
    except ValueError:
        print("Годы должны быть целыми числами.")
        return

    if not validate_years(start_year, end_year):
        return

    results = search_by_genre_and_year(genre, start_year, end_year)
    if results:
        format_table(results, headers=["Название", "Год выпуска"])
    else:
        print("Ничего не найдено.")

def handle_keyword_search():
    keyword = input("\nВведите ключевое слово: ")
    if not validate_keyword(keyword):
        return

    results = search_by_keyword(keyword)
    if results:
        format_table(results, headers=["Название", "Год", "Жанр"])
    else:
        print("Нет совпадений по ключевому слову.")