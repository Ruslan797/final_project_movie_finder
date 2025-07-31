from dotenv import load_dotenv
from pymongo import MongoClient
import os

# Загружаем .env
load_dotenv()

# Получаем строку подключения
MONGO_URI = os.getenv("MONGO_URI")  # Заменить на имя твоей переменной, если другое

try:
    client = MongoClient(MONGO_URI)
    db = client.get_default_database()
    print("Успешное подключение к MongoDB:", db.name)

    # Проверим наличие коллекции и количество документов
    log_collection = db["final_project_210225_buievskyi"]
    print("Документов в коллекции:", log_collection.count_documents({}))

except Exception as e:
    print("Ошибка подключения:", e)