from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes
)

from config import BOT_TOKEN
from logging_config import setup_logging, log_startup_info, log_shutdown_info
from handlers import (
    start, handle_start_button, menu, button_callback,
    waiting_name, waiting_company, waiting_phone, waiting_email,
    search_vendor, cancel, handle_text_message,
    start_vendor_search, handle_profile_edit,
    
    WAITING_NAME, WAITING_COMPANY, WAITING_PHONE, WAITING_EMAIL,
    ADMIN_SEND_MESSAGE, ADMIN_UPDATE_VENDOR, VENDOR_SEARCH,
    ADMIN_SELECT_USERS, ADMIN_MESSAGE_CONTENT,
    
    admin_users, admin_stats, admin_send_start, admin_send_message,
    admin_select_recipients, admin_process_user_ids, admin_pending_users, admin_approve_user
)

logger = setup_logging()

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"❌ ОШИБКА: {context.error}", exc_info=context.error)
    
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "Произошла ошибка. Попробуйте еще раз или обратитесь к администратору."
            )
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение об ошибке: {e}")

def main():
    """Основная функция запуска бота"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    registration_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            MessageHandler(filters.Regex(r'^🚀 СТАРТ$'), handle_start_button)
        ],
        states={
        WAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, waiting_name)],
        WAITING_COMPANY: [MessageHandler(filters.TEXT & ~filters.COMMAND, waiting_company)],
        WAITING_PHONE: [
            MessageHandler(filters.CONTACT, waiting_phone),  
            MessageHandler(filters.TEXT & ~filters.COMMAND, waiting_phone)  
        ],
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
        entry_points=[
            CommandHandler('send', admin_send_start),
            MessageHandler(filters.Regex(r'^📚 Сделать рассылку$'), admin_send_start)
        ],
        states={
            ADMIN_SELECT_USERS: [
                CallbackQueryHandler(admin_select_recipients, pattern=r'^broadcast_'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, admin_process_user_ids)
            ],
            ADMIN_MESSAGE_CONTENT: [
                MessageHandler(
                    (filters.TEXT | filters.PHOTO | filters.Document.ALL | filters.VIDEO) & ~filters.COMMAND,
                    admin_send_message
                )
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        name="admin_broadcast"
    )
    
    application.add_handler(registration_handler)
    application.add_handler(vendor_search_handler)
    application.add_handler(admin_broadcast_handler)
    
    application.add_handler(CommandHandler('menu', menu))
    application.add_handler(CommandHandler('users', admin_users))
    application.add_handler(CommandHandler('stats', admin_stats))
    application.add_handler(CommandHandler('cancel', cancel))
    application.add_handler(CommandHandler('approve', admin_approve_user))
    application.add_handler(CommandHandler('pending', admin_pending_users))
    
    application.add_handler(CallbackQueryHandler(button_callback))
    
    application.add_error_handler(error_handler)
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    
    log_startup_info()
    
    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log_shutdown_info()
    except Exception as e:
        logger.critical(f"💥 КРИТИЧЕСКАЯ ОШИБКА: {e}", exc_info=True)
        raise