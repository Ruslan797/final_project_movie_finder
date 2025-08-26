import os
from dotenv import load_dotenv

# Получение базовой директории и загрузка переменных окружения из .env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOTENV_PATH = os.path.join(BASE_DIR, '..', '.env')
load_dotenv(DOTENV_PATH)

# Константы для подключения к MySQL и MongoDB
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'final_project_group_fullname')