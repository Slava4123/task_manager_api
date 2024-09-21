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
#Создание миграций
alembic init -t async app/migrations

#Настройте базу данных, внесите необходимые изменения в настройки подключения, если необходимо.
#Запустите приложение:
uvicorn app.main:app --reload

#Эндпоинты
Аутентификация
POST /auth/token: Получить токен для аутентификации.
#Пользователи
Список пользователейGET /usersВозвращает список всех пользователей.
Получение пользователяGET /users/{user_id}Возвращает информацию о пользователе по его ID.
Создание пользователяPOST /usersСоздает нового пользователя. Необходимо передать name, email, и password.
Обновление пользователяPUT /users/{user_id}Обновляет информацию о пользователе.
Удаление пользователяDELETE /users/{user_id}Удаляет пользователя.
#Задачи
Создание задачиPOST /tasksСоздает новую задачу. Необходимо передать данные задачи, включая status (можно использовать: "Новая", "В процессе", "Завершена").
Получение задачGET /tasksВозвращает список задач, связанных с текущим пользователем.
Обновление задачиPUT /tasks/{task_id}Обновляет информацию о задаче.
Удаление задачиDELETE /tasks/{task_id}Удаляет задачу.

#Использование
Для тестирования API можно использовать инструменты, такие как Postman или cURL. Не забудьте передать пользователя JSON Web Token для доступа к защищенным маршрутам.

Внесение изменений
# Curl Для User
curl -X 'GET' \
  'http://127.0.0.1:8000/users' \
  -H 'accept: application/json # Получим всех пользователей

curl -X 'GET' \
  'http://127.0.0.1:8000/users/2' \
  -H 'accept: application/json' # Получение определенного пользователя

curl -X 'POST' \
  'http://127.0.0.1:8000/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string",
  "email": "user2@example.com",
  "password": "string"

}' # Создание польвателя (Создаться пользователь "name": "string", "email": "user2@example.com", "password": "string")
curl - X 'PUT' \
  'http://127.0.0.1:8000/users/4' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Adrian",
  "email": "adrian@example.com",
  "password": "123456"
}' # Обновление информации о пользователе

DELETE \
  'http://127.0.0.1:8000/users/4' \
  -H 'accept: */*' # Удаление пользователя

# Curl Для задач
curl -X 'GET' \
  'http://127.0.0.1:8000/task' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJTbGF2YSIsImlkIjoxLCJleHAiOjE3MjY0MTA1NTB9.0l1soiUS1ZNdLUVnTra9cShBddO3f-tdakP43bAZqCg' # Посмотреть все задачи

curl -X 'POST' \
  'http://127.0.0.1:8000/task' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJTbGF2YSIsImlkIjoxLCJleHAiOjE3MjY0MTA1NTB9.0l1soiUS1ZNdLUVnTra9cShBddO3f-tdakP43bAZqCg' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Проверка",
  "description": "string",
  "status": "В процессе"
}' # Создание задачи

curl -X 'PUT' \
  'http://127.0.0.1:8000/task/6' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJTbGF2YSIsImlkIjoxLCJleHAiOjE3MjY0MTA1NTB9.0l1soiUS1ZNdLUVnTra9cShBddO3f-tdakP43bAZqCg' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "Завершена"
}' # Обновление статуса задачи

curl -X 'DELETE' \
  'http://127.0.0.1:8000/task/6' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJTbGF2YSIsImlkIjoxLCJleHAiOjE3MjY0MTA1NTB9.0l1soiUS1ZNdLUVnTra9cShBddO3f-tdakP43bAZqCg' # Удаление задачи







"# FastAPI2" 
