from pymongo import MongoClient
from datetime import datetime, timezone

# Подключение к MongoDB
try:
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
    client.admin.command("ping")  # Проверка подключения
    print("Успешное подключение к MongoDB.")
except Exception as e:
    print(f"Ошибка подключения к MongoDB: {e}")
    client = None

# Настройка базы данных и коллекции
if client:
    db = client["ich"]
    log_collection = db["final_project_210225_buievskyi"]
else:
    log_collection = None

def write_log(search_type, params, results_count):
    """
    Сохраняет информацию о поисковом запросе в MongoDB.

    :param search_type: str — тип запроса ('keyword', 'genre', и т.д.)
    :param params: dict — параметры запроса (например, {'keyword': 'love'})
    :param results_count: int — количество найденных результатов
    """
    if log_collection is None:
        print("Логирование отключено: нет подключения к MongoDB.")
        return

    log_entry = {
        "timestamp": datetime.now(timezone.utc),
        "search_type": search_type,
        "params": params,
        "results_count": results_count
    }

    try:
        log_collection.insert_one(log_entry)
        print("Запрос успешно сохранён в MongoDB.")
    except Exception as e:
        print(f"Ошибка при сохранении запроса: {e}")