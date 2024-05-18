# UsersTasks_bot

## Установка проекта

Создание виртуального окружения
```
python -m venv venv
```

Запуск виртуального окружения в командной строке (windows)
```
venv\Scripts\activate.bat
```

Установка необходимых зависимостей
```
pip install -r requirements.txt
```

### Необходимо создать файл с названием ".env" и добавить в него следующие строки:
```
BOT_TOKEN = ТОКЕН ВАШЕГО ТГ БОТА


POSTGRES_USER = пользователь postgres с правами суперюзера
POSTGRES_PASSWORD = пароль от пользователя postgres с правами суперюзера
DB_HOST = хост базы данных postgresql
DB_NAME = название базы данных postgresql

SQLALCHEMY_URL = postgresql+asyncpg://ИМЯПОЛЬЗОВАТЕЛЯ:ПАРОЛЬ@ХОСТ:ПОРТ/ИМЯ_БД
```

## Запуск бота
```
python main.py
```





