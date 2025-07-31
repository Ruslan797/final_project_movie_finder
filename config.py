from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.getenv("DB_HOST")
MYSQL_PORT = int(os.getenv("DB_PORT", "3306"))
MYSQL_DATABASE = os.getenv("DB_NAME")
MYSQL_USER = os.getenv("DB_USER")
MYSQL_PASSWORD = os.getenv("DB_PASSWORD")

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")