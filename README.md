# Проект: Task Management API

## Описание

Этот проект представляет собой API для управления задачами, созданный с использованием FastAPI и SQLAlchemy. Пользователи могут создавать, обновлять, удалять свои задачи и управлять своими учетными записями через RESTful интерфейс.

## Стек технологий

- **FastAPI**: фреймворк для создания API на Python.
- **SQLAlchemy**: ORM для работы с базами данных.
- **Sqlite**: используемая СУБД (можно адаптировать под любую другую).
- **Passlib**: библиотека для безопасного хеширования паролей.
- **JSON Web Token (JWT)**: для аутентификации пользователей.
- **Alembic**: Создание миграций
## Установка

1. Склонируйте репозиторий:
```bash
   git clone  https://github.com/Slava4123/FastAPI.git;

#Создайте виртуальное окружение и активируйте его
python -m venv venv
   source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
poetry install

#Создание миграций
alembic init -t async app/migrations

#Настройте базу данных, внесите необходимые изменения в настройки подключения, если необходимо.
#Запустите приложение:
uvicorn app.main:app --reload

#Эндпоинты
Аутентификация
POST /auth/token: Получить токен для аутентификации.
#Пользователи
Список пользователей GET /users Возвращает список всех пользователей.
Получение пользователя GET /users/{user_id} Возвращает информацию о пользователе по его ID.
Создание пользователя POST /users Создает нового пользователя. Необходимо передать name, email, и password.
Обновление пользователя PUT /users/{user_id} Обновляет информацию о пользователе.
Удаление пользователя DELETE /users/{user_id} Удаляет пользователя.
#Задачи
Создание задачи POST /tasks Создает новую задачу. Необходимо передать данные задачи, включая status (можно использовать: "Новая", "В процессе", "Завершена").
Получение задач GET /tasks Возвращает список задач, связанных с текущим пользователем.
Обновление задачи PUT /tasks/{task_id} Обновляет информацию о задаче.
Удаление задачи DELETE /tasks/{task_id} Удаляет задачу.

#Использование
Для тестирования API можно использовать инструменты, такие как Postman или cURL. Не забудьте передать пользователя JSON Web Token для доступа к защищенным маршрутам.

Внесение изменений
# Curl Для User
curl -X 'GET' \
  'http://127.0.0.1:8000/users' \
  -H 'accept: application/json' # Получим всех пользователей

curl -X 'GET' \
  'http://127.0.0.1:8000/users/3' \
  -H 'accept: application/json' # Получение определенного пользователя

curl -X 'POST' \
  'http://127.0.0.1:8000/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string2",
  "email": "user2@example.com",
  "password": "string2"
}' # Создание пользователя

}' # Создание польвателя (Создаться пользователь "name": "string", "email": "user2@example.com", "password": "string")
curl - X 'PUT' \
  'http://127.0.0.1:8000/users/2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Adrian",
  "email": "adrian@example.com",
  "password": "123456"
}' # Обновление информации о пользователе

DELETE \
  'http://127.0.0.1:8000/users/3' \
  -H 'accept: */*' # Удаление пользователя

# Curl Для задач
curl -X 'GET' \
  'http://127.0.0.1:8000/task' \
  -H 'accept: application/json' \
  
curl -X 'POST' \
  'http://127.0.0.1:8000/task' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Проверка",
  "description": "string",
  "status": "В процессе"
}' # Создание задачи

curl -X 'PUT' \
  'http://127.0.0.1:8000/task/6' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "Завершена"
}' # Обновление статуса задачи

curl -X 'DELETE' \
  'http://127.0.0.1:8000/task/6' \
  -H 'accept: application/json'  # Удаление задачи

#Получение ключа
curl -X 'POST' \
  'http://127.0.0.1:8000/auth/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=string&password=string&scope=&client_id=string&client_secret=string'
