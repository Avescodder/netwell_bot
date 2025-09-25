"""
Обработчики команд и сообщений для бота Netwell
"""

import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from db import db
from config import ADMIN_IDS, MESSAGES, DIRECTIONS, MANAGERS_CONTACTS, PRODUCT_PORTFOLIO_PATH, GUIDELINE_PATH, LOGOS_URL, MARKETING_PRESENTATION_PATH

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
    
    db_user = db.add_user(user.id, user.username, user.first_name, user.last_name)
    db.log_user_action(user.id, 'start_command')
    
    if db_user.full_name and db_user.company:
        await show_main_menu(update, context)
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
    keyboard = []
    for i in range(0, len(DIRECTIONS), 2):
        row = []
        row.append(InlineKeyboardButton(DIRECTIONS[i], callback_data=f"direction_{DIRECTIONS[i]}"))
        if i + 1 < len(DIRECTIONS):
            row.append(InlineKeyboardButton(DIRECTIONS[i + 1], callback_data=f"direction_{DIRECTIONS[i + 1]}"))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Выберите направление:",
        reply_markup=reply_markup
    )
    db.log_user_action(update.effective_user.id, 'directions_viewed')

async def handle_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка раздела 'Техподдержка'"""
    keyboard = [
        [InlineKeyboardButton("💾 СХД", callback_data="support_storage")],
        [InlineKeyboardButton("🖥 Серверное оборудование", callback_data="support_servers")],
        [InlineKeyboardButton("🔒 Fortinet", callback_data="support_fortinet")],
        [InlineKeyboardButton("🛡 Palo Alto Networks", callback_data="support_palo_alto")],
        [InlineKeyboardButton("📦 Складская программа NetApp", callback_data="support_netapp")],
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
        [InlineKeyboardButton("📊 Маркетинговые возможности", callback_data="marketing_presentation")],
        [InlineKeyboardButton("📞 Контакты маркетинга", callback_data="marketing_contacts")],
        [InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "В данном разделе вы можете получить информацию обо всех возможностях и преимуществах маркетинговых активностей компании:",
        reply_markup=reply_markup
    )
    db.log_user_action(update.effective_user.id, 'marketing_viewed')

async def handle_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка раздела 'Отправить запрос'"""
    keyboard = []
    for i in range(0, len(DIRECTIONS), 2):
        row = []
        row.append(InlineKeyboardButton(DIRECTIONS[i], callback_data=f"request_{DIRECTIONS[i]}"))
        if i + 1 < len(DIRECTIONS):
            row.append(InlineKeyboardButton(DIRECTIONS[i + 1], callback_data=f"request_{DIRECTIONS[i + 1]}"))
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
        await update.message.reply_text(
            vendor.to_card_text(),
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
    keyboard = [
        [InlineKeyboardButton("👤 Имя и Фамилия", callback_data="edit_name")],
        [InlineKeyboardButton("🏢 Компания", callback_data="edit_company")],
        [InlineKeyboardButton("📱 Телефон", callback_data="edit_phone")],
        [InlineKeyboardButton("📧 Email", callback_data="edit_email")],
        [InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Выберите, что бы вы хотели изменить:",
        reply_markup=reply_markup
    )
    db.log_user_action(update.effective_user.id, 'profile_edit_viewed')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик callback-кнопок"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
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
    
    elif data.startswith("direction_"):
        direction = data.replace("direction_", "")
        await show_vendors_by_direction(query, context, direction)
        db.log_user_action(user_id, 'direction_viewed', direction)
    
    elif data.startswith("vendor_"):
        vendor_name = data.replace("vendor_", "")
        vendor = db.get_vendor(vendor_name)
        if vendor:
            await query.edit_message_text(
                vendor.to_card_text(),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Назад", callback_data=f"direction_{vendor.direction}")
                ]])
            )
            db.log_user_action(user_id, 'vendor_card_viewed', vendor.name)
    
    elif data.startswith("request_"):
        direction = data.replace("request_", "")
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
    vendors = db.get_vendors_by_direction(direction)
    
    if not vendors:
        await query.edit_message_text(
            f"По направлению '{direction}' вендоры пока не добавлены.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
            ]])
        )
        return
    
    text = f"**{direction}**\n\nНиже представлены решения вендоров по данному направлению. Нажмите на интересующего вендора, чтобы узнать подробнее.\n\n"
    
    keyboard = []
    for vendor in vendors:
        description = vendor.description[:50] + "..." if vendor.description and len(vendor.description) > 50 else vendor.description or ""
        text += f"• **{vendor.name}** - {description}\n"
        keyboard.append([InlineKeyboardButton(vendor.name, callback_data=f"vendor_{vendor.name}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")])
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_support_info(query, context: ContextTypes.DEFAULT_TYPE, support_type: str):
    """Показать информацию о технической поддержке"""
    support_texts = {
        'storage': """**Сервисная поддержка СХД**

**Включено:**
• Регистрация заявок по телефону или электронной почте
• Технические консультации
• Выезд инженера на площадку заказчика (при необходимости)
• Удаленная поддержка с диагностикой и устранением неисправностей
• Предоставление деталей оборудования на замену

**Приоритеты:**
🔴 **Приоритет 1** (время реакции: 2 часа)
СХД находится в нерабочем состоянии, доступ к данным невозможен

🟡 **Приоритет 2** (время реакции: 4 часа)
Периодические проблемы с функциональностью или производительностью

🟢 **Приоритет 3** (время реакции: 24 часа)
Незначительные проблемы, влияющие на скорость обработки

🔵 **Приоритет 4** (время реакции: 48 часов)
Запросы на консультации по настройке и оптимизации""",
        
        'servers': """**Сервисная поддержка серверного оборудования**

**Включено:**
• Регистрация заявок по телефону или электронной почте
• Технические консультации
• Выезд инженера на площадку заказчика (при необходимости)
• Удаленная поддержка с диагностикой и устранением неисправностей
• Предоставление деталей оборудования на замену

**Приоритеты:**
🔴 **Приоритет 1** (время реакции: 2 часа)
Сервер находится в нерабочем состоянии

🟡 **Приоритет 2** (время реакции: 4 часа)
Периодические проблемы с функциональностью

🟢 **Приоритет 3** (время реакции: 24 часа)
Незначительные проблемы""",
        
        'fortinet': """**Сервисная поддержка по Fortinet**

**Включено:**
• Регистрация заявок 24x7 по телефону или email
• Технические консультации
• Диагностика и устранение неисправностей
• Замена оборудования обсуждается дополнительно

**Приоритеты:**
🔴 **Приоритет 1** (время реакции: 6 часов)
МСЭ находится в нерабочем состоянии, критическое влияние на бизнес

🟡 **Приоритет 2** (время реакции: 24 часа)
Нерегулярные проблемы без влияния на бизнес

🟢 **Приоритет 3** (время реакции: 72 часа)
Запросы на консультации""",
        
        'palo_alto': """**Сервисная поддержка по Palo Alto Networks**

**Включено:**
• Техническая поддержка через веб-портал и телефон
• Управление кейсами для всех моделей NGFW
• Замена неисправных частей (RMA)
• Доступ к документации и FAQ
• Обновления подписок и ПО

**Приоритеты:**
🔴 **Приоритет 1** (< 1 рабочего часа)
Полная неработоспособность, критичные бизнес-процессы остановлены

🟡 **Приоритет 2** (< 4 рабочих часов)
Проблемы затрагивают, но не останавливают критичные процессы

🟢 **Приоритет 3** (< 8 рабочих часов)
Проблемы не затрагивают критичные процессы

🔵 **Приоритет 4** (< 16 рабочих часов)
Информационные запросы, помощь в конфигурации""",
        
        'netapp': """**Складская программа NetApp**

**1. Гибридные системы (HDD)** - дешевле, но медленнее:
• Entry level FAS 2750
• Middle FAS 8300
• Enterprise FAS 9000

**2. ALL FLASH FAS (SSD)** - дороже, но быстрее:
• All flash массив А150
• NVME All flash массив А250
• All flash массив А400
• All flash массив А700
• NVME All flash массив А800
• C800, C250

**3. All SAN Array** (блочный доступ):
• ASA A400
• ASA A700
• ASA A150
• ASA A250"""
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
        await query.edit_message_text(
            f"Ошибка при отправке файла: {str(e)}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
            ]])
        )

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    text = update.message.text
    
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
    else:
        await update.message.reply_text(
            "Выберите пункт из меню или воспользуйтесь командой /menu"
        )
    
    return ConversationHandler.END

# =================== АДМИН ФУНКЦИИ ===================

async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Админская команда для просмотра пользователей"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("У вас нет прав доступа к этой команде.")
        return
    
    users = db.get_all_users()
    
    if not users:
        await update.message.reply_text("Пользователей не найдено.")
        return
    
    text = "👥 **Список пользователей:**\n\n"
    for user in users[:20]: 
        text += f"**ID:** {user.user_id}\n"
        text += f"**Имя:** {user.full_name or 'Не указано'}\n"
        text += f"**Компания:** {user.company or 'Не указана'}\n"
        text += f"**Телефон:** {user.phone or 'Не указан'}\n"
        text += f"**Email:** {user.email or 'Не указан'}\n"
        text += f"**Дата регистрации:** {user.registration_date.strftime('%d.%m.%Y') if user.registration_date else 'Неизвестно'}\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n"
    
    if len(users) > 20:
        text += f"\n... и еще {len(users) - 20} пользователей"
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Админская команда для просмотра статистики"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("У вас нет прав доступа к этой команде.")
        return
    
    stats = db.get_user_stats()
    
    text = "📊 **Статистика бота:**\n\n"
    text += f"👥 Всего пользователей: {stats['total_users']}\n"
    text += f"✅ Активных пользователей: {stats['active_users']}\n\n"
    
    if stats['popular_actions']:
        text += "🔥 **Популярные действия за неделю:**\n"
        for action, count in sorted(stats['popular_actions'].items(), key=lambda x: x[1], reverse=True)[:10]:
            text += f"• {action}: {count}\n"
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def admin_send_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало рассылки сообщения"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("У вас нет прав доступа к этой команде.")
        return ConversationHandler.END
    
    await update.message.reply_text(
        "Введите текст сообщения для рассылки всем пользователям:",
        reply_markup=ReplyKeyboardRemove()
    )
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
            print(f"Ошибка отправки пользователю {user.user_id}: {e}")
    
    await update.message.reply_text(
        f"Рассылка завершена!\n✅ Успешно: {success_count}\n❌ Ошибок: {error_count}"
    )
    
    db.log_user_action(update.effective_user.id, 'admin_broadcast', f'sent to {success_count} users')
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

