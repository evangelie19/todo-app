from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import bson

#  Определение модели задачи


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None


app = FastAPI()

# Mount the static directory to the path /static
app.mount("/static", StaticFiles(directory="static"), name="static")


# Настройте список разрешенных источников (можно использовать ["*"] для разрешения всех источников)
origins = [
    "http://localhost",
    "http://localhost:8080",
]


# Активируйте middleware для поддержки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешите все методы или укажите конкретный список
    # Разрешите все заголовки или укажите конкретный список
    allow_headers=["*"],
)

# Глобальная переменная для хранения ссылки на базу данных
db = None


@app.get("/", response_class=FileResponse)
async def read_index():
    return FileResponse("static/index.html")

# События для подключения и отключения от MongoDB


@app.on_event("startup")
async def startup_db_client():
    global db
    # Создаем подключение к базе данных
    client = AsyncIOMotorClient("mongodb://db:27017")
    db = client["todo_db"]  # Использование базы данных с именем "todo_db"


@app.on_event("shutdown")
async def shutdown_db_client():
    # Закрытие подключения к базе данных
    db.client.close()

# Эндпоинты для CRUD операций


@app.post("/tasks/")
async def create_task(task: TaskUpdate):
    document = task.dict()
    result = await db['tasks'].insert_one(document)
    return {"id": str(result.inserted_id)}


@app.get("/tasks/")
async def read_tasks():
    tasks = []
    cursor = db['tasks'].find()
    async for document in cursor:
        document['id'] = str(document['_id'])
        del document['_id']
        tasks.append(document)
    return tasks


@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task_update: TaskUpdate):

    try:
        obj_id = bson.ObjectId(task_id)
    except bson.errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid task ID")

    # Получаем текущую задачу
    existing_task = await db['tasks'].find_one({"_id": obj_id})

    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task = existing_task.copy()
    # Исключаем поля, которые не установлены
    updated_task.update(task_update.dict(exclude_unset=True))

    # Обновляем задачу в базе данных
    result = await db['tasks'].replace_one({"_id": obj_id}, updated_task)

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task updated successfully"}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    try:
        obj_id = bson.ObjectId(task_id)
    except bson.errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid task ID")

    result = await db['tasks'].delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}


@app.delete("/tasks/")
async def delete_all_tasks():
    # This will delete all documents in the 'tasks' collection
    await db['tasks'].delete_many({})
    return {"message": "All tasks deleted successfully"}
