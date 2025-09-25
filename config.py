"""
Конфигурация бота Netwell
"""

import os
from typing import List

BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

ADMIN_IDS: List[int] = [
    123456789, 

]

DATABASE_URL = 'sqlite:///netwell_bot.db'

FILES_DIR = 'files'
PRODUCT_PORTFOLIO_PATH = f'{FILES_DIR}/product_portfolio.pdf'
GUIDELINE_PATH = f'{FILES_DIR}/guideline.pdf'
LOGOS_URL = 'https://netwell.ru/logos'  
MARKETING_PRESENTATION_PATH = f'{FILES_DIR}/marketing_presentation.pdf'

MESSAGES = {
    'welcome': "Уважаемый коллега, мы создали бот, который станет вашим гидом по компании Netwell. Для доступа в меню нажмите кнопку СТАРТ.",
    'form_intro': "Заполните короткую анкету, чтобы мы могли познакомиться ближе.",
    'form_complete': "Спасибо! Теперь вам доступен полный путеводитель по компании и ее портфелю решений. Нажмите кнопку МЕНЮ, чтобы получить информацию о Netwell, найти информацию о направлениях или конкретном вендоре или изменить свои данные.",
    'profile_updated': "Спасибо, ваши данные изменены!",
    'marketing_contacts': """По общим вопросам обращайтесь в отдел маркетинга Netwell, на почту: marketing@netwell.ru

Для персональных запросов свяжитесь с Ольгой Михеевой, руководителем отдела маркетинга Netwell. Почта: omikheeva@netwell.ru""",
    'request_intro': "Выберете интересующее направление, для получения контактов ответственного Sale-менеджера.",
    'support_intro': """Мы предоставляем профессиональную сервисную поддержку для оборудования ведущих западных производителей в области СХД, серверных и сетевых решений.

Выберите интересующее направление, чтобы узнать подробности.

Услуга платная и приобретается отдельно, а для некоторых решений предоставляется на исключительных условиях по запросу."""
}

DIRECTIONS = [
    'СХД', 'Сервера', 'ИБ', 'Инженерная инфраструктура', 'Сети', 'Унифицированные коммуникации'
]

MANAGERS_CONTACTS = {
    'СХД': 'Иван Петров, Старший менеджер, ipetrov@netwell.ru',
    'Сервера': 'Мария Сидорова, Ведущий менеджер, msidorova@netwell.ru',
    'ИБ': 'Алексей Козлов, Специалист по ИБ, akozlov@netwell.ru',
    'Инженерная инфраструктура': 'Отдел инфраструктуры, infrastructure@netwell.ru',
    'Сети': 'Отдел сетевых решений, networks@netwell.ru',
    'Унифицированные коммуникации': 'Отдел коммуникаций, communications@netwell.ru'
}

os.makedirs(FILES_DIR, exist_ok=True)