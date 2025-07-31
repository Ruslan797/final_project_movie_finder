from pymongo.collection import Collection
from typing import List, Dict

def get_top_queries(log_collection: Collection, limit: int = 5) -> List[Dict]:
    pipeline = [
        {"$group": {
            "_id": "$params",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    try:
        return list(log_collection.aggregate(pipeline))
    except Exception as e:
        print("Ошибка при получении популярных запросов:", e)
        return []

def get_recent_queries(log_collection: Collection, limit: int = 5) -> List[Dict]:
    pipeline = [
        {"$sort": {"timestamp": -1}},
        {"$group": {
            "_id": "$params",
            "latest": {"$first": "$timestamp"}
        }},
        {"$sort": {"latest": -1}},
        {"$limit": limit}
    ]
    try:
        return list(log_collection.aggregate(pipeline))
    except Exception as e:
        print("Ошибка при получении последних запросов:", e)
        return []