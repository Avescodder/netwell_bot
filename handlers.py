"""
Исправленные обработчики команд и сообщений для бота Netwell
"""

import os
import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from db import db
from config import ADMIN_IDS, MESSAGES, DIRECTIONS, MANAGERS_CONTACTS, PRODUCT_PORTFOLIO_PATH, GUIDELINE_PATH, LOGOS_URL, MARKETING_PRESENTATION_PATH

logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
WAITING_NAME, WAITING_COMPANY, WAITING_PHONE, WAITING_EMAIL = range(4)
EDIT_NAME, EDIT_COMPANY, EDIT_PHONE, EDIT_EMAIL = range(4, 8)
ADMIN_SEND_MESSAGE, ADMIN_UPDATE_VENDOR = range(8, 10)
VENDOR_SEARCH = range(10, 11)

def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь администратором"""
    return user_id in ADMIN_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    status = is_admin(user_id=user.id)
    
    db_user = db.add_user(user.id, user.username, user.first_name, user.last_name)
    db.log_user_action(user.id, 'start_command')
    
    if db_user.full_name and db_user.company:
        await show_main_menu(update, context)
        return ConversationHandler.END
    
    elif status:
        await admin_menu_main(update, context)
        return ConversationHandler.END

    keyboard = [['🚀 СТАРТ']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        MESSAGES['welcome'],
        reply_markup=reply_markup
    )
    
    return ConversationHandler.END

async def handle_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатия кнопки СТАРТ"""
    if update.message.text == '🚀 СТАРТ':
        await update.message.reply_text(
            MESSAGES['form_intro'],
            reply_markup=ReplyKeyboardRemove()
        )
        await update.message.reply_text("Введите ваше имя и фамилию:")
        return WAITING_NAME
    return ConversationHandler.END

async def admin_menu_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Основное меню для админа"""
    keyboard = [
        ['🏢 Посмотреть пользователей', '🔍 Посмотреть статистику'],
        ['📚 Сделать рассылку', '🛠 Поменять инфо'],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Выберите интересующий раздел:",
        reply_markup=reply_markup
    )

async def waiting_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание ввода имени и фамилии"""
    context.user_data['full_name'] = update.message.text
    await update.message.reply_text("Введите название вашей компании:")
    return WAITING_COMPANY

async def waiting_company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание ввода компании"""
    context.user_data['company'] = update.message.text
    await update.message.reply_text("Введите ваш мобильный телефон:")
    return WAITING_PHONE

async def waiting_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание ввода телефона"""
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("Введите ваш email:")
    return WAITING_EMAIL

async def waiting_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидание ввода email и завершение регистрации"""
    user_id = update.effective_user.id
    
    db.update_user_profile(
        user_id,
        full_name=context.user_data['full_name'],
        company=context.user_data['company'],
        phone=context.user_data['phone'],
        email=update.message.text
    )
    
    db.log_user_action(user_id, 'profile_completed')
    
    await update.message.reply_text(MESSAGES['form_complete'])
    await show_main_menu(update, context)
    
    return ConversationHandler.END

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать главное меню"""
    keyboard = [
        ['🏢 О компании', '🔍 Поиск вендоров'],
        ['📚 Изучить направления', '🛠 Техподдержка'],
        ['📊 Маркетинг', '📞 Отправить запрос'],
        ['👤 Изменить анкету']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Выберите интересующий раздел:",
        reply_markup=reply_markup
    )
    db.log_user_action(update.effective_user.id, 'main_menu_viewed')

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /menu"""
    await show_main_menu(update, context)

async def handle_company_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка раздела 'О компании'"""
    keyboard = [
        [InlineKeyboardButton("📄 Продуктовый портфель", callback_data="product_portfolio")],
        [InlineKeyboardButton("📋 Гайдлайн", callback_data="guideline")],
        [InlineKeyboardButton("🎨 Логотипы", callback_data="logos")],
        [InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Выберите нужный файл:",
        reply_markup=reply_markup
    )
    db.log_user_action(update.effective_user.id, 'company_info_viewed')

async def handle_directions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка раздела 'Изучить направления'"""
    try:
        keyboard = []
        for i in range(0, len(DIRECTIONS), 2):
            row = []
            direction1 = DIRECTIONS[i]
            row.append(InlineKeyboardButton(direction1, callback_data=f"dir_{i}"))
            if i + 1 < len(DIRECTIONS):
                direction2 = DIRECTIONS[i + 1]
                row.append(InlineKeyboardButton(direction2, callback_data=f"dir_{i + 1}"))
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Выберите направление:",
            reply_markup=reply_markup
        )
        db.log_user_action(update.effective_user.id, 'directions_viewed')
        
    except Exception as e:
        logger.error(f"Error in handle_directions: {e}")
        await update.message.reply_text(
            "Произошла ошибка при загрузке направлений. Попробуйте позже."
        )
        await show_main_menu(update, context)

async def handle_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка раздела 'Техподдержка'"""
    keyboard = [
        [InlineKeyboardButton("💾 СХД", callback_data="support_storage")],
        [InlineKeyboardButton("🖥 Серверы", callback_data="support_servers")],
        [InlineKeyboardButton("🔒 Fortinet", callback_data="support_fortinet")],
        [InlineKeyboardButton("🛡 Palo Alto", callback_data="support_palo_alto")],
        [InlineKeyboardButton("📦 NetApp", callback_data="support_netapp")],
        [InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        MESSAGES['support_intro'],
        reply_markup=reply_markup
    )
    db.log_user_action(update.effective_user.id, 'support_viewed')

async def handle_marketing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка раздела 'Маркетинг'"""
    keyboard = [
        [InlineKeyboardButton("📊 Возможности", callback_data="marketing_presentation")],
        [InlineKeyboardButton("📞 Контакты", callback_data="marketing_contacts")],
        [InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "В данном разделе вы можете получить информацию обо всех возможностях маркетинговых активностей компании:",
        reply_markup=reply_markup
    )
    db.log_user_action(update.effective_user.id, 'marketing_viewed')

async def handle_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка раздела 'Отправить запрос'"""
    keyboard = []
    for i in range(0, len(DIRECTIONS), 2):
        row = []
        row.append(InlineKeyboardButton(DIRECTIONS[i], callback_data=f"req_{i}"))
        if i + 1 < len(DIRECTIONS):
            row.append(InlineKeyboardButton(DIRECTIONS[i + 1], callback_data=f"req_{i + 1}"))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        MESSAGES['request_intro'],
        reply_markup=reply_markup
    )
    db.log_user_action(update.effective_user.id, 'request_viewed')

async def start_vendor_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало поиска вендора"""
    await update.message.reply_text(
        "Введите название компании:",
        reply_markup=ReplyKeyboardRemove()
    )
    db.log_user_action(update.effective_user.id, 'vendor_search_started')
    return VENDOR_SEARCH

async def search_vendor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Поиск вендора в базе данных"""
    vendor_name = update.message.text
    vendor = db.get_vendor(vendor_name)
    
    if vendor:
        card_text = vendor.to_card_text()
        if len(card_text) > 4000:
            card_text = card_text[:4000] + "..."
        
        await update.message.reply_text(
            card_text,
            parse_mode=ParseMode.MARKDOWN
        )
        db.log_user_action(update.effective_user.id, 'vendor_found', vendor.name)
    else:
        await update.message.reply_text(
            f"Вендор '{vendor_name}' не найден в базе данных. "
            "Попробуйте изменить запрос или обратитесь к администратору."
        )
        db.log_user_action(update.effective_user.id, 'vendor_not_found', vendor_name)
    
    await show_main_menu(update, context)
    return ConversationHandler.END

async def handle_profile_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка изменения анкеты"""
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    
    if not user:
        await update.message.reply_text("Пользователь не найден. Начните с команды /start")
        return
    
    profile_text = f"📋 **Ваша анкета:**\n\n"
    profile_text += f"👤 **Имя:** {user.full_name or 'Не указано'}\n"
    profile_text += f"🏢 **Компания:** {user.company or 'Не указана'}\n"
    profile_text += f"📱 **Телефон:** {user.phone or 'Не указан'}\n"
    profile_text += f"📧 **Email:** {user.email or 'Не указан'}\n\n"
    profile_text += "Выберите, что хотите изменить:"
    
    keyboard = [
        [InlineKeyboardButton("👤 Имя и Фамилия", callback_data="edit_name")],
        [InlineKeyboardButton("🏢 Компания", callback_data="edit_company")],
        [InlineKeyboardButton("📱 Телефон", callback_data="edit_phone")],
        [InlineKeyboardButton("📧 Email", callback_data="edit_email")],
        [InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        profile_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )
    db.log_user_action(update.effective_user.id, 'profile_edit_viewed')

# =================== ФУНКЦИИ РЕДАКТИРОВАНИЯ ПРОФИЛЯ ===================

async def edit_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Редактирование имени пользователя"""
    new_name = update.message.text.strip()
    user_id = update.effective_user.id
    
    db.update_user_profile(user_id, full_name=new_name)
    db.log_user_action(user_id, 'profile_name_updated', new_name)
    
    await update.message.reply_text(f"Имя успешно изменено на: {new_name}")
    await show_main_menu(update, context)
    return ConversationHandler.END

async def edit_company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Редактирование компании пользователя"""
    new_company = update.message.text.strip()
    user_id = update.effective_user.id
    
    db.update_user_profile(user_id, company=new_company)
    db.log_user_action(user_id, 'profile_company_updated', new_company)
    
    await update.message.reply_text(f"Компания успешно изменена на: {new_company}")
    await show_main_menu(update, context)
    return ConversationHandler.END

async def edit_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Редактирование телефона пользователя"""
    new_phone = update.message.text.strip()
    user_id = update.effective_user.id
    
    db.update_user_profile(user_id, phone=new_phone)
    db.log_user_action(user_id, 'profile_phone_updated', new_phone)
    
    await update.message.reply_text(f"Телефон успешно изменен на: {new_phone}")
    await show_main_menu(update, context)
    return ConversationHandler.END

async def edit_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Редактирование email пользователя"""
    new_email = update.message.text.strip()
    user_id = update.effective_user.id
    
    db.update_user_profile(user_id, email=new_email)
    db.log_user_action(user_id, 'profile_email_updated', new_email)
    
    await update.message.reply_text(f"Email успешно изменен на: {new_email}")
    await show_main_menu(update, context)
    return ConversationHandler.END

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик callback-кнопок"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    try:
        if data == "back_to_menu":
            await query.message.delete()
            await show_main_menu_callback(query, context)
        
        elif data == "product_portfolio":
            await send_file(query, PRODUCT_PORTFOLIO_PATH, "Продуктовый портфель")
            db.log_user_action(user_id, 'file_downloaded', 'product_portfolio')
        
        elif data == "guideline":
            await send_file(query, GUIDELINE_PATH, "Гайдлайн")
            db.log_user_action(user_id, 'file_downloaded', 'guideline')
        
        elif data == "logos":
            await query.edit_message_text(
                f"Логотипы доступны по ссылке: {LOGOS_URL}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
                ]])
            )
            db.log_user_action(user_id, 'logos_viewed')
        
        elif data.startswith("dir_"):
            dir_index = int(data.replace("dir_", ""))
            direction = DIRECTIONS[dir_index]
            await show_vendors_by_direction(query, context, direction)
            db.log_user_action(user_id, 'direction_viewed', direction)
        
        elif data.startswith("vendor_"):
            try:
                vendor_id = int(data.replace("vendor_", ""))
                vendor = db.get_vendor_by_id(vendor_id)
                if vendor:
                    card_text = vendor.to_card_text()
                    if len(card_text) > 4000:
                        card_text = card_text[:4000] + "..."
                    
                    # Находим индекс направления безопасно
                    try:
                        dir_index = DIRECTIONS.index(vendor.direction)
                        back_callback = f"dir_{dir_index}"
                    except ValueError:
                        back_callback = "back_to_menu"
                    
                    await query.edit_message_text(
                        card_text,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton("🔙 Назад", callback_data=back_callback)
                        ]])
                    )
                    db.log_user_action(user_id, 'vendor_card_viewed', vendor.name)
                else:
                    await query.edit_message_text(
                        "Информация о компании не найдена.",
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu")
                        ]])
                    )
            except (ValueError, Exception) as e:
                logger.error(f"Error processing vendor callback: {e}")
                await query.edit_message_text(
                    "Произошла ошибка при загрузке информации о компании.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu")
                    ]])
                )
        
        elif data.startswith("req_"):
            dir_index = int(data.replace("req_", ""))
            direction = DIRECTIONS[dir_index]
            contact = MANAGERS_CONTACTS.get(direction, "Контакт не найден")
            await query.edit_message_text(
                f"**{direction}**\n\n{contact}",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
                ]])
            )
            db.log_user_action(user_id, 'manager_contact_viewed', direction)
        
        elif data == "marketing_presentation":
            await send_file(query, MARKETING_PRESENTATION_PATH, "Маркетинговая презентация")
            db.log_user_action(user_id, 'file_downloaded', 'marketing_presentation')
        
        elif data == "marketing_contacts":
            await query.edit_message_text(
                MESSAGES['marketing_contacts'],
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
                ]])
            )
            db.log_user_action(user_id, 'marketing_contacts_viewed')
        
        elif data.startswith("support_"):
            support_type = data.replace("support_", "")
            await show_support_info(query, context, support_type)
            db.log_user_action(user_id, 'support_info_viewed', support_type)
        
        # === ОБРАБОТКА РЕДАКТИРОВАНИЯ ПРОФИЛЯ ===
        elif data == "edit_name":
            await query.edit_message_text("Введите новое имя и фамилию:")
            context.user_data['editing_field'] = 'full_name'
            
        elif data == "edit_company":
            await query.edit_message_text("Введите новое название компании:")
            context.user_data['editing_field'] = 'company'
            
        elif data == "edit_phone":
            await query.edit_message_text("Введите новый номер телефона:")
            context.user_data['editing_field'] = 'phone'
            
        elif data == "edit_email":
            await query.edit_message_text("Введите новый email:")
            context.user_data['editing_field'] = 'email'
    
    except Exception as e:
        logger.error(f"Error in button_callback: {e}")
        await query.edit_message_text(
            "Произошла ошибка. Попробуйте еще раз.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu")
            ]])
        )

async def show_main_menu_callback(query, context: ContextTypes.DEFAULT_TYPE):
    """Показать главное меню через callback"""
    keyboard = [
        ['🏢 О компании', '🔍 Поиск вендоров'],
        ['📚 Изучить направления', '🛠 Техподдержка'],
        ['📊 Маркетинг', '📞 Отправить запрос'],
        ['👤 Изменить анкету']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await context.bot.send_message(
        chat_id=query.from_user.id,
        text="Выберите интересующий раздел:",
        reply_markup=reply_markup
    )

async def show_vendors_by_direction(query, context: ContextTypes.DEFAULT_TYPE, direction: str):
    """Показать вендоров по направлению"""
    try:
        vendors = db.get_vendors_by_direction(direction)
        
        if not vendors:
            await query.edit_message_text(
                f"По направлению '{direction}' вендоры пока не добавлены.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
                ]])
            )
            return
        
        text = f"**{direction}**\n\nВыберите вендора для получения подробной информации:\n\n"
        
        keyboard = []
        for vendor in vendors[:10]:
            description = vendor.description[:40] + "..." if vendor.description and len(vendor.description) > 40 else vendor.description or ""
            text += f"• **{vendor.name}** - {description}\n"
            keyboard.append([InlineKeyboardButton(vendor.name, callback_data=f"vendor_{vendor.id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")])
        
        if len(text) > 4000:
            text = text[:4000] + "..."
        
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
    except Exception as e:
        logger.error(f"Error in show_vendors_by_direction: {e}")
        await query.edit_message_text(
            "Произошла ошибка при загрузке вендоров.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
            ]])
        )

async def show_support_info(query, context: ContextTypes.DEFAULT_TYPE, support_type: str):
    """Показать информацию о технической поддержке"""
    support_texts = {
        'storage': """**Сервисная поддержка СХД**

**Включено:**
• Регистрация заявок по телефону/email
• Технические консультации
• Выезд инженера (при необходимости)
• Удаленная поддержка и диагностика
• Замена деталей оборудования

**Приоритеты:**
🔴 **Приоритет 1** (2 часа) - Полная неработоспособность СХД
🟡 **Приоритет 2** (4 часа) - Периодические проблемы
🟢 **Приоритет 3** (24 часа) - Незначительные проблемы
🔵 **Приоритет 4** (48 часов) - Консультации""",
        
        'servers': """**Сервисная поддержка серверов**

**Включено:**
• Регистрация заявок по телефону/email
• Технические консультации
• Выезд инженера (при необходимости)
• Удаленная поддержка
• Замена деталей

**Приоритеты:**
🔴 **Приоритет 1** (2 часа) - Сервер неработоспособен
🟡 **Приоритет 2** (4 часа) - Периодические проблемы
🟢 **Приоритет 3** (24 часа) - Незначительные проблемы""",
        
        'fortinet': """**Сервисная поддержка Fortinet**

**Включено:**
• Регистрация заявок 24x7
• Технические консультации
• Диагностика и устранение проблем
• Замена оборудования (отдельно)

**Приоритеты:**
🔴 **Приоритет 1** (6 часов) - Критическое влияние на бизнес
🟡 **Приоритет 2** (24 часа) - Нерегулярные проблемы
🟢 **Приоритет 3** (72 часа) - Консультации""",
        
        'palo_alto': """**Сервисная поддержка Palo Alto Networks**

**Включено:**
• Техподдержка через портал/телефон
• Управление кейсами для NGFW
• Замена неисправных частей (RMA)
• Доступ к документации
• Обновления ПО и подписок

**Приоритеты:**
🔴 **Приоритет 1** (<1 час) - Критичные процессы остановлены
🟡 **Приоритет 2** (<4 часа) - Затрагивают процессы
🟢 **Приоритет 3** (<8 часов) - Не критично
🔵 **Приоритет 4** (<16 часов) - Консультации""",
        
        'netapp': """**Складская программа NetApp**

**Гибридные системы (HDD):**
• Entry level FAS 2750
• Middle FAS 8300
• Enterprise FAS 9000

**ALL FLASH FAS (SSD):**
• All flash А150, А250, А400
• NVME А700, А800
• C800, C250

**All SAN Array:**
• ASA A150, A250
• ASA A400, A700"""
    }
    
    text = support_texts.get(support_type, "Информация не найдена")
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
        ]])
    )

async def send_file(query, file_path: str, file_description: str):
    """Отправка файла пользователю"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                await query.message.reply_document(
                    document=file,
                    caption=file_description
                )
        else:
            await query.edit_message_text(
                f"Файл '{file_description}' временно недоступен. Обратитесь к администратору.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
                ]])
            )
    except Exception as e:
        logger.error(f"Error sending file: {e}")
        await query.edit_message_text(
            "Ошибка при отправке файла.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
            ]])
        )

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    text = update.message.text
    user_id = update.effective_user.id
    
    if 'editing_field' in context.user_data:
        field = context.user_data['editing_field']
        new_value = text.strip()
        
        # Обновляем профиль
        update_data = {field: new_value}
        db.update_user_profile(user_id, **update_data)
        db.log_user_action(user_id, f'profile_{field}_updated', new_value)
        
        del context.user_data['editing_field']
        
        # Уведомляем об успешном обновлении
        field_names = {
            'full_name': 'Имя',
            'company': 'Компания', 
            'phone': 'Телефон',
            'email': 'Email'
        }
        field_name = field_names.get(field, field)
        
        await update.message.reply_text(f"✅ {field_name} успешно изменен на: {new_value}")
        await show_main_menu(update, context)
        return
    
    elif 'send_to_everyone' in context.user_data:
        del context.user_data['send_to_everyone']
        await admin_send_message(update, context)
        return 
    
    
    if text == '🏢 О компании':
        await handle_company_info(update, context)
    elif text == '🔍 Поиск вендоров':
        return await start_vendor_search(update, context)
    elif text == '📚 Изучить направления':
        await handle_directions(update, context)
    elif text == '🛠 Техподдержка':
        await handle_support(update, context)
    elif text == '📊 Маркетинг':
        await handle_marketing(update, context)
    elif text == '📞 Отправить запрос':
        await handle_request(update, context)
    elif text == '👤 Изменить анкету':
        await handle_profile_edit(update, context)
    elif text == '🏢 Посмотреть пользователей':
        await admin_users(update, context)
    elif text == '🔍 Посмотреть статистику':
        await admin_stats(update, context)
    elif text == '📚 Сделать рассылку':
        await admin_send_start(update, context)
    elif text == '🛠 Поменять инфо':
        await admin_update_vendor_start(update, context)
    else:
        await update.message.reply_text(
            "Выберите пункт из меню или воспользуйтесь командой /menu"
        )
    
    return ConversationHandler.END

# =================== АДМИН ФУНКЦИИ ===================

async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Админская команда для просмотра пользователей"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("У вас нет прав доступа к этой команде.")
        return
    
    users = db.get_all_users()
    
    if not users:
        await update.message.reply_text("Пользователей не найдено.")
        return
    
    text = f"👥 **Список пользователей ({len(users)} чел.):**\n\n"
    for user in users[:20]:
        text += f"**ID:** {user.user_id}\n"
        text += f"**Имя:** {user.full_name or 'Не указано'}\n"
        text += f"**Компания:** {user.company or 'Не указана'}\n"
        text += f"**Телефон:** {user.phone or 'Не указан'}\n"
        text += f"**Email:** {user.email or 'Не указан'}\n"
        text += f"**Дата:** {user.registration_date.strftime('%d.%m.%Y') if user.registration_date else 'Неизвестно'}\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n"
    
    if len(users) > 20:
        text += f"\n... и еще {len(users) - 20} пользователей"
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Админская команда для просмотра статистики"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("У вас нет прав доступа к этой команде.")
        return
    
    try:
        stats = db.get_user_stats()
        
        text = "📊 Статистика бота:\n\n"
        text += f"👥 Всего пользователей: {stats['total_users']}\n"
        text += f"✅ Активных пользователей: {stats['active_users']}\n\n"
        
        if stats['popular_actions']:
            text += "🔥 Популярные действия за неделю:\n"
            for action, count in sorted(stats['popular_actions'].items(), key=lambda x: x[1], reverse=True)[:10]:
                # Экранируем проблемные символы
                clean_action = str(action).replace('*', '').replace('_', '').replace('`', '')
                text += f"• {clean_action}: {count}\n"
        else:
            text += "📈 Действий за неделю пока нет\n"
        
        # Отправляем без parse_mode для избежания ошибок
        await update.message.reply_text(text)
        
    except Exception as e:
        logger.error(f"Error in admin_stats: {e}")
        await update.message.reply_text(
            "❌ Ошибка при получении статистики. Проверьте логи."
        )

async def admin_send_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало рассылки сообщения"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("У вас нет прав доступа к этой команде.")
        return ConversationHandler.END
    
    await update.message.reply_text(
        "Введите текст сообщения для рассылки всем пользователям:",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data['send_to_everyone'] = 1
    return ADMIN_SEND_MESSAGE

async def admin_send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Рассылка сообщения всем пользователям"""
    message_text = update.message.text
    users = db.get_all_users()
    
    success_count = 0
    error_count = 0
    
    await update.message.reply_text(f"Начинаю рассылку {len(users)} пользователям...")
    
    for user in users:
        try:
            await context.bot.send_message(
                chat_id=user.user_id,
                text=f"📢 **Сообщение от администрации Netwell:**\n\n{message_text}",
                parse_mode=ParseMode.MARKDOWN
            )
            success_count += 1
        except Exception as e:
            error_count += 1
            logger.error(f"Ошибка отправки пользователю {user.user_id}: {e}")
    
    await update.message.reply_text(
        f"Рассылка завершена!\n✅ Успешно: {success_count}\n❌ Ошибок: {error_count}"
    )
    
    db.log_user_action(update.effective_user.id, 'admin_broadcast', f'sent to {success_count} users')
    await admin_menu_main(update, context)
    return ConversationHandler.END

async def admin_update_vendor_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало обновления вендора"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("У вас нет прав доступа к этой команде.")
        return ConversationHandler.END
    
    await update.message.reply_text(
        "Введите данные вендора в формате:\n\n"
        "Название|Направление|Описание|Приоритет|Происхождение|Год|Продукты\n\n"
        "Пример:\n"
        "NetApp|СХД|Лидер в области систем хранения данных|Высокий|США|1992|FAS, AFF, ONTAP",
        reply_markup=ReplyKeyboardRemove()
    )
    return ADMIN_UPDATE_VENDOR

async def admin_update_vendor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обновление информации о вендоре"""
    try:
        data_parts = update.message.text.split('|')
        
        if len(data_parts) < 3:
            await update.message.reply_text(
                "Неверный формат. Минимум: Название|Направление|Описание"
            )
            return ConversationHandler.END
        
        vendor_data = {
            'name': data_parts[0].strip(),
            'direction': data_parts[1].strip(),
            'description': data_parts[2].strip(),
            'priority': data_parts[3].strip() if len(data_parts) > 3 else None,
            'origin': data_parts[4].strip() if len(data_parts) > 4 else None,
            'founded_year': int(data_parts[5].strip()) if len(data_parts) > 5 and data_parts[5].strip().isdigit() else None,
            'key_products': data_parts[6].strip() if len(data_parts) > 6 else None,
        }
        
        vendor = db.add_vendor(**vendor_data)
        
        await update.message.reply_text(
            f"✅ Вендор '{vendor.name}' успешно добавлен/обновлен!"
        )
        
        db.log_user_action(update.effective_user.id, 'admin_vendor_updated', vendor.name)
        
    except Exception as e:
        logger.error(f"Error updating vendor: {e}")
        await update.message.reply_text(f"Ошибка при обновлении вендора: {str(e)}")
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена текущей операции"""
    await update.message.reply_text(
        "Операция отменена.",
        reply_markup=ReplyKeyboardRemove()
    )
    await show_main_menu(update, context)
    return ConversationHandler.END