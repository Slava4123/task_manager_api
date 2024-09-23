# Проект: API для управления задачами

## Описание

Данный проект представляет собой API для управления задачами, созданный с использованием **FastAPI** и **SQLAlchemy**. Пользователи могут создавать, обновлять и удалять свои задачи, а также управлять своими учетными записями через RESTful интерфейс.

## Стек технологий

- **FastAPI**: Фреймворк для создания API на Python.
- **SQLAlchemy**: ORM для работы с базами данных.
- **SQLite**: Используемая СУБД (можно адаптировать под любую другую).
- **Passlib**: Библиотека для безопасного хеширования паролей.
- **JSON Web Token (JWT)**: Для аутентификации пользователей.
- **Alembic**: Создание миграций базы данных.

## Установка

1. **Склонируйте репозиторий**:
 
   git clone https://github.com/Slava4123/FastAPI.git
   


2. **Создайте виртуальное окружение и активируйте его**:
 
   python -m venv venv
   # Для Linux/Mac
   source venv/bin/activate
   # Для Windows
   venv\Scripts\activate
   


3. **Установите зависимости**:
 
   poetry install
   


4. **Создайте миграции**:
 
   alembic init -t async app/migrations
   


5. **Настройте базу данных**, внесите необходимые изменения в настройки подключения, если это необходимо.

6. **Запустите приложение**:
 
   uvicorn app.main:app --reload
   


## Структура проекта

```
task_manager_api/                # Корневая директория проекта
├── app/                          # Основная директория приложения
│   ├── database/                 # Настройки подключения к БД и создание сессий
│   │   ├── db.py                 # Основные настройки базы данных
│   │   └── db_session.py          # Файл для управления сеансами
│   ├── migrations/                # Миграции Alembic
│   │   └── env.py                # Конфигурации Alembic
│   ├── models/                    # Определение моделей (SQLAlchemy)
│   │   ├── users.py               # Модель пользователя
│   │   └── tasks.py               # Модель задачи
│   ├── routers/                   # Роутеры для API
│   │   ├── __init__.py            # Подключение роутеров
│   │   ├── users.py               # Роуты для пользователей
│   │   ├── tasks.py               # Роуты для задач
│   │   └── auth.py                # Функции аутентификации и работы с JWT
│   ├── __init__.py                # Инициализация приложения
│   ├── schemas.py                 # Определение схем (Pydantic)
│   ├── main.py                    # Главный файл приложения
│   └── utils.py                   # Утилиты и вспомогательные функции
├── tests/                         # Тесты
│   ├── conftest.py                # Общие настройки для тестов
│   ├── test_users.py              # Тесты для пользователей
│   ├── test_main.py               # Тесты для главного приложения
│   └── test_auth_user.py          # Тесты для аутентификации пользователей
├── alembic.ini                    # Конфигурация Alembic
├── poetry.lock                    # Зависимости проекта (если используется Poetry)
├── pyproject.toml                 # Конфигурация проекта (если используется Poetry)
└── README.md                      # Документация проекта
```


## Эндпоинты

### Аутентификация

- **POST /auth/token**: Получить токен для аутентификации.

### Пользователи

- **GET /users**: Возвращает список всех пользователей.
- **GET /users/{user_id}**: Возвращает информацию о пользователе по его ID.
- **POST /users**: Создает нового пользователя (передайте `name`, `email`, и `password`).
- **PUT /users/{user_id}**: Обновляет информацию о пользователе.
- **DELETE /users/{user_id}**: Удаляет пользователя.

### Задачи

- **POST /tasks**: Создает новую задачу (необходимо передать данные задачи, включая `status`, который может быть: "Новая", "В процессе", "Завершена").
- **GET /tasks**: Возвращает список задач, связанных с текущим пользователем.
- **PUT /tasks/{task_id}**: Обновляет информацию о задаче.
- **DELETE /tasks/{task_id}**: Удаляет задачу.

## Использование cURL

Для тестирования API можно использовать инструменты, такие как Postman или cURL. Не забудьте передать JSON Web Token для доступа к защищенным маршрутам.

### Примеры использования с помощью cURL

#### Работа с пользователями

1. **Получение списка пользователей**:
 
   curl -X 'GET' \
     'http://127.0.0.1:8000/users' \
     -H 'accept: application/json'
   


2. **Получение информации о пользователе**:
 
   curl -X 'GET' \
     'http://127.0.0.1:8000/users/3' \
     -H 'accept: application/json'
   


3. **Создание пользователя**:
 
   curl -X 'POST' \
     'http://127.0.0.1:8000/users' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
       "name": "string2",
       "email": "user2@example.com",
       "password": "string2"
     }'
   


4. **Обновление информации о пользователе**:
 
   curl -X 'PUT' \
     'http://127.0.0.1:8000/users/2' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
       "name": "Adrian",
       "email": "adrian@example.com",
       "password": "123456"
     }'
   


5. **Удаление пользователя**:
 
   curl -X 'DELETE' \
     'http://127.0.0.1:8000/users/3' \
     -H 'accept: */*'
   


#### Работа с задачами

1. **Получение списка задач**:
 
   curl -X 'GET' \
     'http://127.0.0.1:8000/tasks' \
     -H 'accept: application/json'
   


2. **Получение информации о задаче**:
 
   curl -X 'GET' \
     'http://127.0.0.1:8000/tasks/2' \
     -H 'accept: application/json'
   


3. **Создание задачи**:
 
   curl -X 'POST' \
     'http://127.0.0.1:8000/tasks' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
       "title": "string",
       "description": "string",
       "status": "Новая"
     }'
   


4. **Обновление информации о задаче**:
 
   curl -X 'PUT' \
     'http://127.0.0.1:8000/tasks/2' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
       "title": "Updated title",
       "description": "Updated description",
       "status": "В процессе"
     }'
   
