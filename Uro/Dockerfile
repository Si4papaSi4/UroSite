# Используем Python 3.10
FROM python:3.10

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект в контейнер
COPY . /app

# Запускаем Gunicorn
CMD ["gunicorn", "Uro.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout","120"]
