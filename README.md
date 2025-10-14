# Netwell Info Bot

Telegram-бот для компании Netwell - интерактивный путеводитель по компании и её портфелю решений.

## Описание

Бот предоставляет сотрудникам и партнерам информацию о:

- Продуктовом портфеле компании
- Вендорах и их решениях
- Технической поддержке по различным направлениям
- Маркетинговых возможностях
- Контактах ответственных менеджеров

Включает встроенную админ-панель для управления пользователями, статистикой и контентом.

## Требования

- Python 3.8+
- SQLite
- Telegram Bot Token

## Установка

```bash
# Клонировать репозиторий или распаковать архив
cd netwell_bot

# Создать виртуальное окружение
python -m venv venv

# Активировать виртуальное окружение
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

## Настройка

Создайте файл `.env` в корневой папке проекта со следующими параметрами:

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
DB_URL=sqlite:///YOUR_NAME.db
ADMIN_IDS=123456789
TABLE_DIRECTIONS_SHEET_ID=https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID -> you have to write here only your sheet id
TABLE_VENDORS_SHEET_ID=https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID  -> you have to write here only your sheet id
LOGOS_URL=https://drive.google.com/drive/folders/YOUR_FOLDER_ID 
PRODUCT_PORTFOLIO_URL=https://drive.google.com/file/d/YOUR_FILE_ID 
```

### Описание параметров

| Параметр | Описание | Как получить |
|----------|----------|--------------|
| `BOT_TOKEN` | Токен вашего Telegram-бота | Создайте бота через @BotFather и скопируйте токен |
| `DB_URL` | Путь к базе данных SQLite | Оставьте значение по умолчанию или укажите свой путь |
| `ADMIN_IDS` | ID администраторов через запятую | Напишите боту @userinfobot, чтобы узнать свой ID |
| `TABLE_DIRECTIONS_SHEET_ID` | Ссылка на Google таблицу с направлениями | Создайте таблицу и вставьте ТОЛКО SHEET_ID |
| `TABLE_VENDORS_SHEET_ID` | Ссылка на Google таблицу с вендорами | Создайте таблицу и вставьте ТОЛЬКО SHEET_ID |
| `LOGOS_URL` | Ссылка на папку с логотипами | Загрузите логотипы на Google Drive и вставьте ссылку |
| `PRODUCT_PORTFOLIO_URL` | Ссылка на PDF с продуктовым портфелем | Загрузите PDF на Google Drive и вставьте ссылку |

### Пример заполнения

```env
BOT_TOKEN=56789012:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw
DB_URL=sqlite:///netwell_bot.db
ADMIN_IDS=123456789,987654321
TABLE_DIRECTIONS_SHEET_ID=1a2b3c4d5e6f7g8h
TABLE_VENDORS_SHEET_ID=9i8h7g6f5e4d
LOGOS_URL=https://drive.google.com/drive/folders/1BxYz2CwDvEu3FgGh4HiIj5JkKl6LmMn7
PRODUCT_PORTFOLIO_URL=https://drive.google.com/file/d/1NoOpPqQrRsStTuUvVwWxXyYzZaAbBcCd
```

## Запуск

```bash

docker-compose up -d --build # or sometimes on macOS ->  docker compose up -d --build                              

```

## База данных

Бот автоматически создает SQLite базу с тремя таблицами:

- `users` - данные пользователей и анкеты
- `vendors` - карточки компаний-вендоров для поиска по названиям 
- `vendors_directions` - карточки компаний для поиска по направлениям 
- `user_logs` - логи действий пользователей

## Поддержка

По вопросам работы бота обращайтесь к morozovvsevolod24@gmail.com.

## Лицензия

Proprietary - для внутреннего использования компанией Netwell.