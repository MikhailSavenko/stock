#!/bin/bash

# Ждем, пока база данных будет доступна
until nc -z db 5432; do
  echo "Ожидание базы данных..."
  sleep 1
done

mkdir -p alembic/versions

# Создание миграции
echo "Создание миграций..."
alembic revision --autogenerate

# Применяем миграции
echo "Применение миграций..."
alembic upgrade head

# Наполним базу товарами
echo "Наполняем базу товарами..."
python fill_db.py

# Запускаем приложение
echo "Запуск приложения..."
uvicorn app.main:app --host 0.0.0.0 --port 8000

