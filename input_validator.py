from tabulate import tabulate

def shorten(text, length=80):
    """
    Обрезает строку до указанной длины и убирает переносы строк для корректного вывода в таблице.
    """
    if not isinstance(text, str):
        return text
    text = text.replace('\n', ' ').replace('\r', ' ')  # убираем переносы строк
    return (text[:length] + '...') if len(text) > length else text

def print_films(films):
    """
    Выводит список фильмов в виде таблицы, обрезая длинные описания для красоты.
    """
    if not films:
        print("Нет фильмов по вашему запросу.")
        return
    headers = ["ID", "Название", "Год", "Описание"]
    rows = [
        (
            f["film_id"],
            shorten(f["title"], 20),
            f["release_year"],
            shorten(f["description"], 80)
        )
        for f in films
    ]
    print(tabulate(rows, headers, tablefmt="grid"))

def print_genres(genres):
    """
    Красиво выводит список жанров (категорий) с их ID.
    """
    if not genres:
        print("Жанры не найдены.")
        return
    print("Доступные жанры:")
    for g in genres:
        print(f'{g["category_id"]:>2}: {g["name"]}')

def safe_int_input(prompt, valid_range=None):
    """
    Безопасный ввод числа (или 'q' для отмены).
    Если указан valid_range, то число должно быть в этом диапазоне.
    """
    while True:
        val = input(prompt).strip()
        if val.lower() == 'q':
            return None
        if val.isdigit():
            val = int(val)
            if (valid_range is None) or (val in valid_range):
                return val
        print("Пожалуйста, введите корректное число или 'q' для отмены.")