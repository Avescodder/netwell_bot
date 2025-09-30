"""
Скрипт быстрой настройки бота Netwell
"""
import os
import sys

def create_env_file():
    """Создание .env файла с настройками"""
    env_content = """# Настройки бота Netwell

# Токен бота (получить у @BotFather)
BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# ID администраторов через запятую (узнать у @userinfobot)
ADMIN_IDS=123456789
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Создан файл .env")

def create_directories():
    """Создание необходимых папок"""
    directories = ['files']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Создана папка: {directory}")

def create_sample_files():
    """Создание примеров файлов"""
    files_info = {
        'files/product_portfolio.pdf': 'Поместите сюда продуктовый портфель',
        'files/guideline.pdf': 'Поместите сюда гайдлайн компании',
        'files/marketing_presentation.pdf': 'Поместите сюда маркетинговую презентацию'
    }
    
    for file_path, description in files_info.items():
        if not os.path.exists(file_path):
            with open(file_path.replace('.pdf', '.txt'), 'w', encoding='utf-8') as f:
                f.write(f"# {description}\n\nЗамените этот файл на реальный PDF.")
            print(f"✅ Создан placeholder: {file_path.replace('.pdf', '.txt')}")

def setup_database():
    """Настройка базы данных"""
    try:
        from db import db
        from sample_vendors import add_sample_vendors
        
        print("✅ База данных инициализирована")
        
        # Добавляем примеры вендоров
        answer = input("Хотите добавить примеры вендоров? (y/n): ")
        if answer.lower() in ['y', 'yes', 'да']:
            add_sample_vendors()
        
        return True
    except Exception as e:
        print(f"❌ Ошибка при настройке базы данных: {e}")
        return False

def main():
    """Основная функция настройки"""
    print("🚀 Настройка бота Netwell\n")
    
    if not os.path.exists('.env'):
        create_env_file()
    else:
        print("ℹ️  Файл .env уже существует")
    
    create_directories()
    
    create_sample_files()
    
    setup_database()
    
    print("\n" + "="*50)
    print("🎉 Настройка завершена!")
    print("\n📋 Что нужно сделать дальше:")
    print("1. Отредактируйте файл .env:")
    print("   - Замените YOUR_BOT_TOKEN_HERE на токен от @BotFather")
    print("   - Замените 123456789 на ваш Telegram ID (узнать у @userinfobot)")
    print("2. Поместите PDF файлы в папку files/")
    print("3. Запустите бота: python bot.py")
    print("4. Протестируйте: python test_bot.py")

if __name__ == "__main__":
    main()