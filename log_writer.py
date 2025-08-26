from pymongo import MongoClient, DESCENDING
from datetime import datetime
from .config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION

def get_collection():
    """
    Получает объект коллекции MongoDB для логирования запросов.
    """
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    return db[MONGO_COLLECTION]

def save_query(query_type, query_data, result_count):
    """
    Сохраняет информацию о поисковом запросе в MongoDB.
    Аргументы:
        query_type (str): Тип запроса ('keyword' или 'genre_year').
        query_data (dict): Параметры запроса.
        result_count (int): Количество найденных фильмов.
    """
    col = get_collection()
    doc = {
        "timestamp": datetime.now(),
        "query_type": query_type,
        "params": query_data,
        "count": result_count
    }
    col.insert_one(doc)

def get_top_queries(n=5):
    """
    Возвращает топ-N самых популярных поисковых запросов (по типу и параметрам).
    Каждый элемент содержит: параметры, количество раз, время последнего запроса.
    """
    col = get_collection()
    pipeline = [
        {"$group": {
            "_id": {"query_type": "$query_type", "params": "$params"},
            "count": {"$sum": 1},
            "last_time": {"$max": "$timestamp"}
        }},
        {"$sort": {"count": -1, "last_time": -1}},
        {"$limit": n}
    ]
    return list(col.aggregate(pipeline))

def get_last_unique_queries(n=5):
    """
    Возвращает последние N уникальных поисковых запросов (по параметрам и типу).
    Каждый элемент содержит: параметры, количество результатов, время.
    """
    col = get_collection()
    pipeline = [
        {"$sort": {"timestamp": -1}},
        {
            "$group": {
                "_id": {"query_type": "$query_type", "params": "$params"},
                "timestamp": {"$first": "$timestamp"},
                "query_type": {"$first": "$query_type"},
                "params": {"$first": "$params"},
                "count": {"$first": "$count"}
            }
        },
        {"$sort": {"timestamp": -1}},
        {"$limit": n}
    ]
    return list(col.aggregate(pipeline))