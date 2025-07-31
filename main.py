from db_connector import (
    search_by_keyword,
    search_by_genre_and_year,
    get_genres,
    get_year_range
)
from log_writer import write_log
from log_stats import get_top_queries, get_recent_queries
from formatter import format_table
from dotenv import load_dotenv

import os


load_dotenv()

def run():
    while True:
        print("\nМеню:")
        print("1. Поиск по ключевому слову")
        print("2. Поиск по жанру и году")
        print("3. Статистика запросов")
        print("4. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            keyword = input("Введите ключевое слово: ")
            offset = 0
            while True:
                results = search_by_keyword(keyword, offset)
                write_log("keyword", {"keyword": keyword}, len(results))
                format_table(results, ["Название"])
                if len(results) < 10 or input("Показать ещё? (y/n) ") != "y":
                    break
                offset += 10

        elif choice == "2":
            genres = get_genres()
            min_year, max_year = get_year_range()
            print(f"\nДоступные жанры: {genres}")
            print(f"Диапазон лет: {min_year} - {max_year}")

            genre = input("Выберите жанр: ")
            start_year = int(input("С какого года: "))
            end_year = int(input("До какого года: "))
            offset = 0

            while True:
                results = search_by_genre_and_year(genre, start_year, end_year, offset)
                write_log("genre_and_year", {
                    "genre": genre, "start_year": start_year, "end_year": end_year
                }, len(results))
                format_table(results, ["Название", "Год выпуска"])
                if len(results) < 10 or input("Показать ещё? (y/n) ") != "y":
                    break
                offset += 10

        elif choice == "3":
            print("\nЧастые запросы:")
            for item in get_top_queries():
                print(item)

            print("\nПоследние запросы:")
            for item in get_recent_queries():
                print(item)

        elif choice == "4":
            print("Выход из программы.До встречи!")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    run()
