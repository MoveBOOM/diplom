# Используем базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем файл .env
COPY .env .env

# Запускаем миграции и собираем статику
RUN python manage.py migrate

# Команда запуска
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]