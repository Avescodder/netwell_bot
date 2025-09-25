# Dockerfile для развертывания бота Netwell

FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование файлов требований
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание папки для файлов
RUN mkdir -p files

# Создание пользователя для запуска (безопасность)
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Порт не нужен для Telegram бота
EXPOSE 8000

# Команда запуска
CMD ["python", "bot.py"]