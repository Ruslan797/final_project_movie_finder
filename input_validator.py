def validate_genre(genre, valid_genres):
    if genre not in valid_genres:
        print("Жанр недоступен.")
        return False
    return True

def validate_years(start, end, min_year=1990, max_year=2025):
    if not isinstance(start, int) or not isinstance(end, int):
        print("Годы должны быть целыми числами.")
        return False
    if start < min_year or end > max_year or start > end:
        print(f"Недопустимый диапазон: от {min_year} до {max_year}.")
        return False
    return True

def validate_keyword(keyword):
    if not keyword or keyword.strip() == "":
        print("Ключевое слово не может быть пустым.")
        return False
    return True