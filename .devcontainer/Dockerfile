# Используем официальный образ Python 3.8
FROM python:3.8-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в рабочую директорию
COPY . /app

# Устанавливаем Git
RUN apt-get update && apt-get install -y git

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir fastapi[all] motor uvicorn

# Определяем команду для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
