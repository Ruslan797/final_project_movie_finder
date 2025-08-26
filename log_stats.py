from . import db_mysql, db_mongo, utils

def _get_genre_dict():
    """
    Вспомогательная функция: возвращает словарь {category_id: name} для всех жанров.
    Используется для красивого вывода статистики запросов.
    """
    genres = db_mysql.get_genres()
    return {g["category_id"]: g["name"] for g in genres}

def _format_params(params, genre_dict=None):
    """
    Вспомогательная функция: форматирует параметры запроса для вывода пользователю.
    """
    if "genre_id" in params and genre_dict:
        genre_id = params["genre_id"]
        genre_name = genre_dict.get(genre_id, f"ID {genre_id}")
        return f"Жанр: {genre_name}, года: {params.get('year_from', '?')}–{params.get('year_to', '?')}"
    if "keyword" in params:
        return f"Ключевое слово: \"{params['keyword']}\""
    return str(params)

def search_by_keyword():
    """
    Режим поиска фильмов по ключевому слову.
    Пользователь может листать страницы (n/p), выйти (q).
    Логирует запрос в MongoDB.
    """
    keyword = input("Введите ключевое слово для поиска в названии фильма: ").strip()
    if not keyword:
        print("Ключевое слово не может быть пустым.")
        return
    offset = 0
    page = 1
    page_size = 10

    # Получаем все результаты для определения количества страниц и для статистики
    all_films = db_mysql.search_by_keyword(keyword, offset=0, limit=1000000)
    total_results = len(all_films)
    total_pages = (total_results + page_size - 1) // page_size if total_results else 1

    while True:
        films = db_mysql.search_by_keyword(keyword, offset=offset, limit=page_size)
        if not films and offset == 0:
            print("Фильмы не найдены.")
            db_mongo.save_query("keyword", {"keyword": keyword}, 0)
            return
        utils.print_films(films)
        print(f"Страница {page} из {total_pages}")
        if offset == 0:
            # Логируем общее количество найденных фильмов, а не только на странице!
            db_mongo.save_query("keyword", {"keyword": keyword}, total_results)
        print("n - следующая страница | p - предыдущая страница | q - выход в меню")
        cmd = input("Выберите действие (n/p/q): ").lower()
        if cmd == "n":
            if (offset + page_size) < total_results:
                offset += page_size
                page += 1
            else:
                print("Больше результатов нет.")
        elif cmd == "p":
            if page > 1:
                offset -= page_size
                page -= 1
            else:
                print("Это первая страница.")
        elif cmd == "q":
            break
        else:
            print("Некорректный ввод!")

def search_by_genre_and_year():
    """
    Режим поиска фильмов по жанру и диапазону годов.
    Пользователь выбирает жанр, вводит годы, листает страницы (n/p), выходит (q).
    Логирует запрос в MongoDB.
    """
    genres = db_mysql.get_genres()
    if not genres:
        print("Нет доступных жанров.")
        return
    utils.print_genres(genres)
    genre_ids = [g["category_id"] for g in genres]
    genre_id = utils.safe_int_input("Введите ID жанра ('q' для отмены): ", genre_ids)
    if genre_id is None:
        print("Отмена поиска.")
        return
    year_range = db_mysql.get_year_range()
    yr_min, yr_max = year_range["min_year"], year_range["max_year"]
    if not yr_min or not yr_max:
        print("Нет информации о годах выпуска.")
        return
    print(f"Введите диапазон лет выпуска (от {yr_min} до {yr_max}).")
    while True:
        year_from = utils.safe_int_input("От года: ")
        year_to = utils.safe_int_input("До года: ")
        if year_from is None or year_to is None:
            print("Отмена поиска.")
            return
        if yr_min <= year_from <= year_to <= yr_max:
            break
        print("Некорректный диапазон лет.")
    offset = 0
    page = 1
    page_size = 10

    # Получаем все результаты для определения количества страниц и для статистики
    all_films = db_mysql.search_by_genre_and_year(genre_id, year_from, year_to, offset=0, limit=1000000)
    total_results = len(all_films)
    total_pages = (total_results + page_size - 1) // page_size if total_results else 1

    while True:
        films = db_mysql.search_by_genre_and_year(genre_id, year_from, year_to, offset=offset, limit=page_size)
        if not films and offset == 0:
            print("Фильмы не найдены.")
            db_mongo.save_query("genre_year", {
                "genre_id": genre_id,
                "year_from": year_from,
                "year_to": year_to
            }, 0)
            return
        utils.print_films(films)
        print(f"Страница {page} из {total_pages}")
        if offset == 0:
            # Логируем общее количество найденных фильмов, а не только на странице!
            db_mongo.save_query("genre_year", {
                "genre_id": genre_id,
                "year_from": year_from,
                "year_to": year_to
            }, total_results)
        print("n - следующая страница | p - предыдущая страница | q - выход в меню")
        cmd = input("Выберите действие (n/p/q): ").lower()
        if cmd == "n":
            if (offset + page_size) < total_results:
                offset += page_size
                page += 1
            else:
                print("Больше результатов нет.")
        elif cmd == "p":
            if page > 1:
                offset -= page_size
                page -= 1
            else:
                print("Это первая страница.")
        elif cmd == "q":
            break
        else:
            print("Некорректный ввод!")

def show_top_queries():
    """
    Показывает топ-5 популярных поисковых запросов (по частоте).
    Красиво форматирует параметры (жанр — по названию).
    """
    print("\n====== ТОП-5 популярных поисковых запросов ======")
    top = db_mongo.get_top_queries(5)
    if not top:
        print("Нет данных о популярных запросах.")
        return
    genre_dict = _get_genre_dict()
    for i, t in enumerate(top, 1):
        qtype = t['_id']['query_type']
        params = t['_id']['params']
        count = t['count']
        time = t['last_time'].strftime('%Y-%m-%d %H:%M:%S')
        params_str = _format_params(params, genre_dict)
        type_disp = "Жанр + годы" if qtype == "genre_year" else "Ключевое слово"
        print(f"{i}) Тип запроса: {type_disp}")
        print(f"   Параметры: {params_str}")
        print(f"   Количество выполнений: {count}")
        print(f"   Последний раз: {time}")
        print("-" * 54)

def show_last_unique_queries():
    """
    Показывает последние 5 уникальных поисковых запросов.
    Красиво форматирует параметры (жанр — по названию).
    """
    print("\n====== Последние 5 уникальных поисковых запросов ======")
    last = db_mongo.get_last_unique_queries(5)
    if not last:
        print("Нет данных о последних запросах.")
        return
    genre_dict = _get_genre_dict()
    for i, t in enumerate(last, 1):
        qtype = t['query_type']
        params = t['params']
        count = t['count']
        time = t['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        params_str = _format_params(params, genre_dict)
        type_disp = "Жанр + годы" if qtype == "genre_year" else "Ключевое слово"
        print(f"{i}) Тип запроса: {type_disp}")
        print(f"   Параметры: {params_str}")
        print(f"   Количество найденных фильмов: {count}")
        print(f"   Время: {time}")
        print("-" * 54)