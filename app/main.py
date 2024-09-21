"""
Основной модуль приложения FastAPI.

В этом модуле создается экземпляр приложения FastAPI,
которое служит основным входом для обработки HTTP-запросов.
Модуль включает в себя маршрутизаторы для пользователей, задач
и аутентификации, а также определяет базовый эндпоинт для проверки
состояния приложения.

Импортируемые классы и модули:
- FastAPI: основной класс для создания веб-приложения.
- 'users': маршруты, связанные с пользователями.
- 'tasks': маршруты, связанные с задачами.
- 'auth': маршруты, связанные с аутентификацией.

Основные функции:
- Создание и конфигурация экземпляра FastAPI.
- Регистрация маршрутизаторов для обработки различных эндпоинтов.
- Определение эндпоинта для проверки состояния приложения
  (health check).

Эндпоинты:
- GET /: Возвращает состояние приложения и временную метку.
"""
from fastapi import FastAPI


from app.routers import users
from app.routers import tasks
from app.routers import auth

app = FastAPI()
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(auth.router)

@app.get('/')
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2024-09-14T12:00:00Z"
    }
