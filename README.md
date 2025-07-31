README = """
Final Project: Film Catalog Search

Поисковый инструмент для фильмов по жанру, году выпуска и ключевым словам.
Проект использует базы данных MongoDB и MySQL, а также реализует логирование действий пользователя.

Структура проекта:
├── config.py              # Загрузка переменных из .env
├── db_connector.py        # Подключение к MongoDB и MySQL
├── formatter.py           # Форматирование вывода в таблицу
├── handlers.py            # Обработка пользовательских запросов
├── input_validator.py     # Проверка корректности ввода
├── log_stats.py           # Статистика логов
├── log_writer.py          # Запись логов
├── main.py                # Точка входа
├── requirements.txt       # Зависимости проекта
├── README.md              # Описание проекта
├── .env                   # Конфиденциальные настройки (не загружается)
└── tests/
    ├── test_connector.py
    └── test_main.py

   Как запустить:

1. Установите зависимости:
   pip install -r requirements.txt

2. Создайте файл .env в корне проекта:
   MONGO_URI=mongodb://localhost:27017
   MONGO_DB=ich
   MONGO_COLLECTION=final_project_210225_buievskyi

   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DB=film_catalog

3. Запустите проект:
   python main.py

  Возможности:

- Поиск фильмов по жанру и диапазону годов
- Поиск по ключевым словам
- Валидация пользовательского ввода
- Логирование действий
- Вывод результатов в виде таблицы

  Тестирование:
   pytest tests/
Автор:
- 
Руслан Буевский  
Группа: 210225  
Проект: final_project_210225_buievskyi

Лицензия:
Проект создан в рамках учебного курса. Использование — свободное.
"""