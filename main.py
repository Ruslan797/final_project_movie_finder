from . import search

def stats_menu():
    """
    Подменю статистики поисковых запросов.
    Позволяет посмотреть топ-5 популярных, последние 5 уникальных или выйти в основное меню.
    """
    while True:
        print("\n=== Статистика запросов ===")
        print("1. Топ-5 популярных запросов")
        print("2. Последние 5 уникальных запросов")
        print("3. Назад в главное меню")
        choice = input("Выберите действие: ")
        if choice == "1":
            try:
                search.show_top_queries()
            except Exception as e:
                print(f"Ошибка вывода популярных запросов: {e}")
        elif choice == "2":
            try:
                search.show_last_unique_queries()
            except Exception as e:
                print(f"Ошибка вывода последних запросов: {e}")
        elif choice == "3":
            return
        else:
            print("Некорректный ввод!")

def main():
    """
    Главное меню приложения.
    Позволяет выбрать режим поиска или статистики, а также выйти.
    """
    while True:
        print("\n=== Поиск фильмов ===")
        print("1. Поиск фильма по ключевому слову")
        print("2. Поиск по жанру и диапазону годов")
        print("3. Статистика запросов")
        print("4. Выход")
        choice = input("Выберите действие: ")
        if choice == "1":
            try:
                search.search_by_keyword()
            except Exception as e:
                print(f"Ошибка поиска: {e}")
        elif choice == "2":
            try:
                search.search_by_genre_and_year()
            except Exception as e:
                print(f"Ошибка поиска: {e}")
        elif choice == "3":
            stats_menu()
        elif choice == "4":
            print("Пока!")
            break
        else:
            print("Некорректный ввод!")

if __name__ == "__main__":
    main()