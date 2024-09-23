Проект: API для управления задачами

###Описание###
Данный проект представляет собой API для управления задачами, созданный с использованием FastAPI и SQLAlchemy. Пользователи могут создавать, обновлять, удалять свои задачи и управлять своими учетными записями через RESTful интерфейс.

###Стек технологий###
FastAPI: фреймворк для создания API на Python.
SQLAlchemy: ORM для работы с базами данных.
Sqlite: используемая СУБД (можно адаптировать под любую другую).
Passlib: библиотека для безопасного хеширования паролей.
JSON Web Token (JWT): для аутентификации пользователей.
Alembic: Создание миграций

###Установка###
Склонируйте репозиторий:
git clone https://github.com/Slava4123/FastAPI.git;
Создайте виртуальное окружение и активируйте его:
python -m venv venv
source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
Установите зависимости:
poetry install
Создайте миграции:
alembic init -t async app/migrations
Настройте базу данных, внесите необходимые изменения в настройки подключения, если необходимо.
Запустите приложение:
uvicorn app.main:app --reload
Эндпоинты

###Аутентификация###
POST /auth/token: Получить токен для аутентификации.

###Пользователи###
GET /users: Возвращает список всех пользователей.
GET /users/{user_id}: Возвращает информацию о пользователе по его ID.
POST /users: Создает нового пользователя. Необходимо передать name, email, и password.
PUT /users/{user_id}: Обновляет информацию о пользователе.
DELETE /users/{user_id}: Удаляет пользователя.

###Задачи###
POST /tasks: Создает новую задачу. Необходимо передать данные задачи, включая status (можно использовать: "Новая", "В процессе", "Завершена").
GET /tasks: Возвращает список задач, связанных с текущим пользователем.
PUT /tasks/{task_id}: Обновляет информацию о задаче.
DELETE /tasks/{task_id}: Удаляет задачу.

###Использование###
Для тестирования API можно использовать инструменты, такие как Postman или cURL. Не забудьте передать пользователя JSON Web Token для доступа к защищенным маршрутам.
Примеры использования с помощью curl

###Пользователи###
Получение списка пользователей:
curl -X 'GET' \
  'http://127.0.0.1:8000/users' \
  -H 'accept: application/json'
Получение информации о пользователе:
curl -X 'GET' \
  'http://127.0.0.1:8000/users/3' \
  -H 'accept: application/json'
Создание пользователя:
curl -X 'POST' \
  'http://127.0.0.1:8000/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "string2",
    "email": "user2@example.com",
    "password": "string2"
  }'
Обновление информации о пользователе:
curl -X 'PUT' \
  'http://127.0.0.1:8000/users/2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Adrian",
    "email": "adrian@example.com",
    "password": "123456"
  }'
Удаление пользователя:
curl -X 'DELETE' \
  'http://127.0.0.1:8000/users/3' \
  -H 'accept: */*'
  
###Задачи###
Получение списка задач:
curl -X 'GET' \
  'http://
  'http://127.0.0.1:8000/auth/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=string&password=string&scope=&client_id=string&client_secret=string'
http://127.0.0.1:8000/tasks \
     -H 'accept: application/json'
Получение информации о задаче:
curl -X 'GET' \
     'http://127.0.0.1:8000/tasks/2' \
     -H 'accept: application/json'
Создание задачи:
curl -X 'POST' \
     'http://127.0.0.1:8000/tasks' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
       "title": "string",
       "description": "string",
       "status": "Новая"
     }'
Обновление информации о задаче:
curl -X 'PUT' \
     'http://127.0.0.1:8000/tasks/2' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
       "title": "Updated title",
       "description": "Updated description",
       "status": "В процессе"
     }'
Удаление задачи:
curl -X 'DELETE' \
     'http://127.0.0.1:8000/tasks/2' \
     -H 'accept: */*'
