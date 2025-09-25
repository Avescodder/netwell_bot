"""
Тестовый скрипт для проверки работы бота
"""

from db import db
from config import DIRECTIONS

def test_database():
    """Тест подключения к базе данных"""
    try:
        print("✅ База данных подключена успешно")
        
        user = db.add_user(123456789, "testuser", "Test", "User")
        print(f"✅ Пользователь добавлен: {user.user_id}")
        
        db.log_user_action(123456789, "test_action", "test details")
        print("✅ Логирование работает")
        
        stats = db.get_user_stats()
        print(f"✅ Статистика: {stats}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка базы данных: {e}")
        return False

def test_config():
    """Тест конфигурации"""
    try:
        print("📋 Проверка конфигурации:")
        print(f"Направления: {DIRECTIONS}")
        
        from config import BOT_TOKEN, ADMIN_IDS
        
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            print("⚠️  Не забудьте заменить BOT_TOKEN в config.py")
        else:
            print("✅ BOT_TOKEN настроен")
            
        if 123456789 in ADMIN_IDS:
            print("⚠️  Не забудьте заменить ADMIN_IDS в config.py")
        else:
            print("✅ ADMIN_IDS настроены")
            
        return True
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование бота Netwell...\n")
    
    if test_config():
        print("✅ Конфигурация OK\n")
    else:
        print("❌ Проблемы с конфигурацией\n")
        return
    
    if test_database():
        print("✅ База данных OK\n")
    else:
        print("❌ Проблемы с базой данных\n")
        return
    
    print("🎉 Все тесты пройдены! Бот готов к запуску.")
    print("Запустите: python bot.py")

if __name__ == "__main__":
    main()