FROM python:3.12.3

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

RUN apt-get update && apt-get install -y netcat-openbsd

COPY . .

# выполнение скрипта
RUN chmod +x /app/start.sh

# Запускаем скрипт при старте контейнера
CMD ["/app/start.sh"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]