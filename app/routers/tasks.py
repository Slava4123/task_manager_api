from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from app.models import Task
from app.schemas import CreateTask, ReadTask, UpdateTask
from app.database.db_session import get_db
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import get_current_user

router = APIRouter(prefix='/task', tags=['Task'])

@router.post('', response_model=CreateTask, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: CreateTask,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Создание новой задачи.

    Аргументы:
        task (CreateTask): Данные задачи для создания.
        db (AsyncSession): Сессия базы данных.
        user (dict): Информация о текущем пользователе.

    Исключения:
        HTTPException: Если статус задачи недопустим.

    Возвращает:
        CreateTask: Созданная задача.
    """
    user_id = user['id']

    # Проверка на допустимый статус задачи
    if task.status not in ["Новая", "В процессе", "Завершена"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Недопустимый статус задачи")
    if (await db.execute(select(Task).where(Task.title == task.title))).scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Задача с таким заголовком уже есть")

    db_task = Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при добавлении задачи в базу данных")
    return db_task

@router.get('', response_model=List[ReadTask])
async def read_tasks(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Получение списка задач текущего пользователя.

    Аргументы:
        db (AsyncSession): Сессия базы данных.
        user (dict): Информация о текущем пользователе.

    Возвращает:
        List[ReadTask]: Список задач.
    """
    user_id = user['id']
    query = select(Task).where(Task.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.get('/{task_id}', response_model=ReadTask)
async def get_task_id(
        task_id: int,
        db: AsyncSession = Depends(get_db),
        user: dict[str, int] = Depends(get_current_user)
) -> ReadTask:
    """
    Получить задачу по ID для текущего пользователя.

    - **task_id**: ID задачи, которую нужно получить.
    - **db**: Асинхронная сессия базы данных.
    - **user**: Информация о текущем пользователе.

    Возвращает объект задачи, если задача найдена; иначе вызывает HTTPException 404.
    """
    user_id = user['id']  # Получаем ID пользователя

    # Выполняем запрос на получение задачи
    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await db.execute(query)
    task = result.scalars().first()  # Получаем первую задачу

    # Проверяем, была ли найдена задача
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return task  # Возвращаем задачу  # Возвращаем задачу

@router.put('/{task_id}', response_model=UpdateTask)
async def update_task(
    task_id: int,
    task: UpdateTask,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Обновление существующей задачи.

    Аргументы:
        task_id (int): Идентификатор задачи для обновления.
        task (UpdateTask): Данные задачи для обновления.
        db (AsyncSession): Сессия базы данных.
        user (dict): Информация о текущем пользователе.

    Исключения:
        HTTPException: Если статус задачи недопустим или задача не найдена.

    Возвращает:
        UpdateTask: Обновленная задача.
    """
    # Проверка на допустимый статус задачи
    if task.status and task.status not in ["Новая", "В процессе", "Завершена"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Недопустимый статус задачи")

    query = select(Task).where(Task.id == task_id, Task.user_id == user['id'])
    result = await db.execute(query)
    db_task = result.scalars().first()

    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)

    await db.commit()
    await db.refresh(db_task)
    return db_task

@router.delete('/{task_id}', response_model=dict)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Удаление существующей задачи.

    Аргументы:
        task_id (int): Идентификатор задачи для удаления.
        db (AsyncSession): Сессия базы данных.
        user (dict): Информация о текущем пользователе.

    Исключения:
        HTTPException: Если задача не найдена.

    Возвращает:
        dict: Словарь с сообщением об успешном удалении задачи.
    """
    query = select(Task).where(Task.id == task_id, Task.user_id == user['id'])
    result = await db.execute(query)
    db_task = result.scalars().first()

    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    await db.delete(db_task)
    await db.commit()
    return {"detail": "Задача успешно удалена"}
