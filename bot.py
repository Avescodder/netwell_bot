"""
Главный файл Telegram-бота для компании Netwell
"""

import logging
from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    ConversationHandler,
    filters
)

from config import BOT_TOKEN
from handlers import (
    start, handle_start_button, menu, button_callback,
    waiting_name, waiting_company, waiting_phone, waiting_email,
    search_vendor, cancel, handle_text_message,
    start_vendor_search,
    
    WAITING_NAME, WAITING_COMPANY, WAITING_PHONE, WAITING_EMAIL,
    ADMIN_SEND_MESSAGE, ADMIN_UPDATE_VENDOR, VENDOR_SEARCH,
    
    admin_users, admin_stats, admin_send_start, admin_send_message,
    admin_update_vendor_start, admin_update_vendor
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Основная функция запуска бота"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # ========== CONVERSATION HANDLERS ==========
    
    registration_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            MessageHandler(filters.Regex(r'^🚀 СТАРТ$'), handle_start_button)
        ],
        states={
            WAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, waiting_name)],
            WAITING_COMPANY: [MessageHandler(filters.TEXT & ~filters.COMMAND, waiting_company)],
            WAITING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, waiting_phone)],
            WAITING_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, waiting_email)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        name="registration"
    )
    
    vendor_search_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex(r'^🔍 Поиск вендоров$'), start_vendor_search)
        ],
        states={
            VENDOR_SEARCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_vendor)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        name="vendor_search"
    )
    
    admin_broadcast_handler = ConversationHandler(
        entry_points=[CommandHandler('send', admin_send_start)],
        states={
            ADMIN_SEND_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_send_message)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        name="admin_broadcast"
    )
    
    admin_vendor_handler = ConversationHandler(
        entry_points=[CommandHandler('update_vendor', admin_update_vendor_start)],
        states={
            ADMIN_UPDATE_VENDOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_update_vendor)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        name="admin_vendor_update"
    )
    
    # ========== ДОБАВЛЯЕМ ОБРАБОТЧИКИ ==========
    
    application.add_handler(registration_handler)
    application.add_handler(vendor_search_handler)
    application.add_handler(admin_broadcast_handler)
    application.add_handler(admin_vendor_handler)
    
    application.add_handler(CommandHandler('menu', menu))
    application.add_handler(CommandHandler('users', admin_users))
    application.add_handler(CommandHandler('stats', admin_stats))
    application.add_handler(CommandHandler('cancel', cancel))
    
    application.add_handler(CallbackQueryHandler(button_callback))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # ========== ЗАПУСК БОТА ==========
    
    logger.info("Запускаем бота Netwell...")
    
    application.run_polling(
        drop_pending_updates=True, 
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise

