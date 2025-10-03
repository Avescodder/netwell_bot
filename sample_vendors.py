# """
# Скрипт для добавления примеров вендоров в базу данных
# Запускать: python sample_vendors.py
# """

# from db import db

# def add_sample_vendors():
#     """Добавление примеров вендоров в базу данных"""
    
#     sample_vendors = [
#         {
#             'name': 'NetApp',
#             'direction': 'СХД',
#             'description': 'Мировой лидер в области систем хранения данных и управления данными',
#             'priority': 'Высокий',
#             'origin': 'США',
#             'founded_year': 1992,
#             'key_products': 'FAS, AFF, ONTAP, Cloud Volumes',
#             'target_customers': 'Enterprise, облачные провайдеры, государственный сектор',
#             'advantages': 'Лидирующие технологии дедупликации, гибридное облако, простота управления',
#             'software_registry': 'Да',
#             'fstek': 'Да',
#             'fsb': 'Нет',
#             'main_competitors': 'Dell EMC, HPE, Pure Storage',
#             'certified_engineers': 'Да',
#             'warehouse_availability': 'Да',
#             'service_provided': 'Да'
#         },
#         {
#             'name': 'Huawei',
#             'direction': 'Сети',
#             'description': 'Ведущий мировой поставщик сетевого оборудования и телекоммуникационных решений',
#             'priority': 'Средний',
#             'origin': 'Китай',
#             'founded_year': 1987,
#             'key_products': 'CloudEngine коммутаторы, NetEngine маршрутизаторы, CloudCampus',
#             'target_customers': 'Корпоративный сектор, операторы связи, государственные учреждения',
#             'advantages': 'Конкурентоспособные цены, широкая линейка продуктов, технологии AI',
#             'software_registry': 'Частично',
#             'fstek': 'Нет',
#             'fsb': 'Нет',
#             'main_competitors': 'Cisco, Juniper, Arista',
#             'certified_engineers': 'Да',
#             'warehouse_availability': 'Да',
#             'service_provided': 'Да'
#         },
#         {
#             'name': 'Fortinet',
#             'direction': 'ИБ',
#             'description': 'Глобальный лидер в области кибербезопасности и сетевой безопасности',
#             'priority': 'Высокий',
#             'origin': 'США',
#             'founded_year': 2000,
#             'key_products': 'FortiGate NGFW, FortiAnalyzer, FortiManager, FortiClient',
#             'target_customers': 'Enterprise, MSSP, государственный сектор',
#             'advantages': 'Высокая производительность, единая платформа безопасности, ASIC процессоры',
#             'software_registry': 'Да',
#             'fstek': 'Да',
#             'fsb': 'Частично',
#             'main_competitors': 'Palo Alto Networks, Check Point, SonicWall',
#             'certified_engineers': 'Да',
#             'warehouse_availability': 'Да',
#             'service_provided': 'Да'
#         },
#         {
#             'name': 'Dell Technologies',
#             'direction': 'Сервера',
#             'description': 'Один из крупнейших производителей серверного оборудования и ИТ-решений',
#             'priority': 'Высокий',
#             'origin': 'США',
#             'founded_year': 1984,
#             'key_products': 'PowerEdge серверы, PowerVault системы хранения, iDRAC',
#             'target_customers': 'Enterprise, SMB, облачные провайдеры',
#             'advantages': 'Надежность, широкая экосистема, глобальная поддержка',
#             'software_registry': 'Частично',
#             'fstek': 'Нет',
#             'fsb': 'Нет',
#             'main_competitors': 'HPE, Lenovo, IBM',
#             'certified_engineers': 'Да',
#             'warehouse_availability': 'Да',
#             'service_provided': 'Да'
#         },
#         {
#             'name': 'Schneider Electric',
#             'direction': 'Инженерная инфраструктура',
#             'description': 'Мировой лидер в области энергетики и автоматизации',
#             'priority': 'Высокий',
#             'origin': 'Франция',
#             'founded_year': 1836,
#             'key_products': 'ИБП Galaxy, APC UPS, EcoStruxure, инфраструктурные решения',
#             'target_customers': 'ЦОД, промышленность, коммерческие здания',
#             'advantages': 'Энергоэффективность, надежность, глобальный сервис',
#             'software_registry': 'Частично',
#             'fstek': 'Нет',
#             'fsb': 'Нет',
#             'main_competitors': 'Eaton, Legrand, ABB',
#             'certified_engineers': 'Да',
#             'warehouse_availability': 'Да',
#             'service_provided': 'Да'
#         },
#         {
#             'name': 'Ростелеком',
#             'direction': 'Унифицированные коммуникации',
#             'description': 'Крупнейший российский оператор связи и поставщик цифровых услуг',
#             'priority': 'Средний',
#             'origin': 'Россия',
#             'founded_year': 1993,
#             'key_products': 'Облачная телефония, видеоконференцсвязь, контакт-центр',
#             'target_customers': 'Государственный сектор, крупный бизнес, SMB',
#             'advantages': 'Российская разработка, соответствие требованиям законодательства',
#             'software_registry': 'Да',
#             'fstek': 'Да',
#             'fsb': 'Да',
#             'main_competitors': 'МТС, МегаФон, Tele2',
#             'certified_engineers': 'Да',
#             'warehouse_availability': 'Нет',
#             'service_provided': 'Да'
#         }
#     ]
    
#     print("Добавляем примеры вендоров в базу данных...")
    
#     for vendor_data in sample_vendors:
#         try:
#             vendor = db.add_vendor(**vendor_data)
#             print(f"✅ Добавлен вендор: {vendor.name} ({vendor.direction})")
#         except Exception as e:
#             print(f"❌ Ошибка при добавлении {vendor_data['name']}: {e}")
    
#     print(f"\nГотово! Добавлено {len(sample_vendors)} вендоров.")
#     print("Теперь можно тестировать поиск и просмотр по направлениям.")

# if __name__ == '__main__':
#     add_sample_vendors()

import requests
import csv
from io import StringIO
from db import db, Vendor

SHEET_ID = "1W5CbaQg1kDf3j0dPDbXzYGGfumXmRhc4EnuZzKZDeis"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

FIELD_MAP = {
    "Вендоры": "name",
    "Приоритет в развитии": "priority",
    "Происхождение вендора": "origin",
    "Год основания": "founded_year",
    "Категории продуктов": "categories",
    "Ключевые продукты": "key_products",
    "Потенциальные заказчики (сектор)": "target_customers",
    "Конкурентные преимущества": "advantages",
    "Включены ли в реестр ПО / ФСТЭК / ФСБ": "software_registry",
    "ФСТЭК": "fstek",
    "ФСБ": "fsb",
    "ЛПР": "decision_makers",
    "Основные конкуренты": "main_competitors",
    "Замена иностранных производителей": "foreign_replacement",
    "Сервисное обслуживание": "service",
    "Партнерская программа (если есть, ключевые условия)": "partner_program",
    "Требования к партнерам": "partner_requirements",
    "Преимущества для партнеров": "partner_benefits",
    "Рекомендации по продажам": "sales_recommendations",
    "Рекомендации по продажам:": "sales_recommendations",
    "Наличие наших сертифицированных инженеров": "certified_engineers",
    "Наличие оборудование на складе Нетвелл": "warehouse_availability",
    "Оказываем ли сервис по вендору?": "service_provided",
    "Наличие вендора у нас на сайте": "vendor_on_our_site",
    "Наличие Нетвелл на сайте вендора": "netwell_on_vendor_site",
}

# Маппинг ключевых слов на направления из DIRECTIONS
KEYWORD_TO_DIRECTION = {
    # СХД
    "схд": "СХД",
    "системы хранения": "СХД",
    "система хранения": "СХД",
    "хранение данных": "СХД",
    "storage": "СХД",
    
    # Сервера
    "серверное оборудование": "Сервера",
    "серверы": "Сервера",
    "сервер": "Сервера",
    
    # ИБ
    "информационная безопасность": "ИБ",
    "безопасность": "ИБ",
    "firewall": "ИБ",
    "ngfw": "ИБ",
    
    # Сети
    "сетевое оборудование": "Сети",
    "сеть": "Сети",
    "коммутатор": "Сети",
    "маршрутизатор": "Сети",
    
    # Инженерная инфраструктура
    "инженерная инфраструктура": "Инженерная инфраструктура",
    "ибп": "Инженерная инфраструктура",
    "источник бесперебойного питания": "Инженерная инфраструктура",
    "кондиционирование": "Инженерная инфраструктура",
    
    # Унифицированные коммуникации
    "унифицированные коммуникации": "Унифицированные коммуникации",
    "видеоконференция": "Унифицированные коммуникации",
    "ip-телефония": "Унифицированные коммуникации",
    
    # ПО
    "программное обеспечение": "ПО",
    "по": "ПО",
    "software": "ПО",
}

def extract_directions_from_categories(categories_text):
    """Извлекает ВСЕ направления из текста категорий продуктов"""
    if not categories_text:
        return []
    
    categories_lower = categories_text.lower()
    found_directions = set()
    
    # Ищем все совпадения с ключевыми словами
    for keyword, direction in KEYWORD_TO_DIRECTION.items():
        if keyword in categories_lower:
            found_directions.add(direction)
    
    return list(found_directions)

def add_vendors_from_sheet():
    print("📥 Загружаем данные из Google Sheets...")
    
    try:
        response = requests.get(CSV_URL)
        response.raise_for_status()
        
        content = response.content.decode('utf-8-sig')
        data = StringIO(content)
        
        lines = list(csv.reader(data))
        
        # Ищем строку с заголовками
        header_row_index = None
        for i, line in enumerate(lines):
            if any("Вендоры" in cell or "вендор" in cell.lower() for cell in line):
                header_row_index = i
                break
        
        if header_row_index is None:
            print("❌ Не найдена строка с заголовками!")
            return
        
        headers = lines[header_row_index]
        data_rows = lines[header_row_index + 1:]
        
        print(f"📊 Найдено строк: {len(data_rows)}")
        
        added_count = 0
        updated_count = 0
        skipped_count = 0
        
        for row_num, row in enumerate(data_rows, start=header_row_index + 2):
            if len(row) < len(headers):
                row.extend([''] * (len(headers) - len(row)))
            
            row_dict = dict(zip(headers, row))
            
            # Ищем название вендора
            vendor_name = None
            for possible_name in ["Вендоры", "Вендор", "Название", "Name"]:
                vendor_name = row_dict.get(possible_name, "").strip()
                if vendor_name:
                    break
            
            if not vendor_name:
                skipped_count += 1
                continue
            
            # Проверяем, существует ли вендор
            existing_vendor = db.session.query(Vendor).filter_by(name=vendor_name).first()
            
            vendor_data = {}
            
            for col_name, field_name in FIELD_MAP.items():
                value = row_dict.get(col_name, "").strip()
                
                if not value:
                    value = None
                
                if field_name == "founded_year" and value:
                    try:
                        value = int(value)
                    except:
                        value = None
                
                if field_name not in vendor_data or vendor_data[field_name] is None:
                    vendor_data[field_name] = value
            
            # Определяем ВСЕ направления из категорий
            directions = []
            if vendor_data.get('categories'):
                directions = extract_directions_from_categories(vendor_data['categories'])
            
            # Сохраняем первое направление в поле direction (для обратной совместимости)
            if directions:
                vendor_data['direction'] = directions[0]
                directions_str = ", ".join(directions)
            else:
                vendor_data['direction'] = None
                directions_str = "⚠️  не определены"
            
            # Используем categories как есть для description
            if not vendor_data.get('description') and vendor_data.get('categories'):
                vendor_data['description'] = vendor_data['categories'][:200]
            
            try:
                vendor = db.add_vendor(**vendor_data)
                
                if existing_vendor:
                    print(f"🔄 Обновлен: {vendor.name} → [{directions_str}]")
                    updated_count += 1
                else:
                    print(f"✅ Добавлен: {vendor.name} → [{directions_str}]")
                    added_count += 1
                    
            except Exception as e:
                print(f"❌ Ошибка при обработке '{vendor_name}' (строка {row_num}): {e}")
                db.session.rollback()
        
        print(f"\n{'='*50}")
        print(f"✅ Добавлено новых: {added_count}")
        print(f"🔄 Обновлено: {updated_count}")
        if skipped_count > 0:
            print(f"⏭️  Пропущено пустых строк: {skipped_count}")
        print(f"{'='*50}")
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    add_vendors_from_sheet()