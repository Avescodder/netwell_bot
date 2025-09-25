"""
Скрипт для добавления примеров вендоров в базу данных
Запускать: python sample_vendors.py
"""

from db import db

def add_sample_vendors():
    """Добавление примеров вендоров в базу данных"""
    
    sample_vendors = [
        {
            'name': 'NetApp',
            'direction': 'СХД',
            'description': 'Мировой лидер в области систем хранения данных и управления данными',
            'priority': 'Высокий',
            'origin': 'США',
            'founded_year': 1992,
            'key_products': 'FAS, AFF, ONTAP, Cloud Volumes',
            'target_customers': 'Enterprise, облачные провайдеры, государственный сектор',
            'advantages': 'Лидирующие технологии дедупликации, гибридное облако, простота управления',
            'software_registry': 'Да',
            'fstek': 'Да',
            'fsb': 'Нет',
            'main_competitors': 'Dell EMC, HPE, Pure Storage',
            'certified_engineers': 'Да',
            'warehouse_availability': 'Да',
            'service_provided': 'Да'
        },
        {
            'name': 'Huawei',
            'direction': 'Сети',
            'description': 'Ведущий мировой поставщик сетевого оборудования и телекоммуникационных решений',
            'priority': 'Средний',
            'origin': 'Китай',
            'founded_year': 1987,
            'key_products': 'CloudEngine коммутаторы, NetEngine маршрутизаторы, CloudCampus',
            'target_customers': 'Корпоративный сектор, операторы связи, государственные учреждения',
            'advantages': 'Конкурентоспособные цены, широкая линейка продуктов, технологии AI',
            'software_registry': 'Частично',
            'fstek': 'Нет',
            'fsb': 'Нет',
            'main_competitors': 'Cisco, Juniper, Arista',
            'certified_engineers': 'Да',
            'warehouse_availability': 'Да',
            'service_provided': 'Да'
        },
        {
            'name': 'Fortinet',
            'direction': 'ИБ',
            'description': 'Глобальный лидер в области кибербезопасности и сетевой безопасности',
            'priority': 'Высокий',
            'origin': 'США',
            'founded_year': 2000,
            'key_products': 'FortiGate NGFW, FortiAnalyzer, FortiManager, FortiClient',
            'target_customers': 'Enterprise, MSSP, государственный сектор',
            'advantages': 'Высокая производительность, единая платформа безопасности, ASIC процессоры',
            'software_registry': 'Да',
            'fstek': 'Да',
            'fsb': 'Частично',
            'main_competitors': 'Palo Alto Networks, Check Point, SonicWall',
            'certified_engineers': 'Да',
            'warehouse_availability': 'Да',
            'service_provided': 'Да'
        },
        {
            'name': 'Dell Technologies',
            'direction': 'Сервера',
            'description': 'Один из крупнейших производителей серверного оборудования и ИТ-решений',
            'priority': 'Высокий',
            'origin': 'США',
            'founded_year': 1984,
            'key_products': 'PowerEdge серверы, PowerVault системы хранения, iDRAC',
            'target_customers': 'Enterprise, SMB, облачные провайдеры',
            'advantages': 'Надежность, широкая экосистема, глобальная поддержка',
            'software_registry': 'Частично',
            'fstek': 'Нет',
            'fsb': 'Нет',
            'main_competitors': 'HPE, Lenovo, IBM',
            'certified_engineers': 'Да',
            'warehouse_availability': 'Да',
            'service_provided': 'Да'
        },
        {
            'name': 'Schneider Electric',
            'direction': 'Инженерная инфраструктура',
            'description': 'Мировой лидер в области энергетики и автоматизации',
            'priority': 'Высокий',
            'origin': 'Франция',
            'founded_year': 1836,
            'key_products': 'ИБП Galaxy, APC UPS, EcoStruxure, инфраструктурные решения',
            'target_customers': 'ЦОД, промышленность, коммерческие здания',
            'advantages': 'Энергоэффективность, надежность, глобальный сервис',
            'software_registry': 'Частично',
            'fstek': 'Нет',
            'fsb': 'Нет',
            'main_competitors': 'Eaton, Legrand, ABB',
            'certified_engineers': 'Да',
            'warehouse_availability': 'Да',
            'service_provided': 'Да'
        },
        {
            'name': 'Ростелеком',
            'direction': 'Унифицированные коммуникации',
            'description': 'Крупнейший российский оператор связи и поставщик цифровых услуг',
            'priority': 'Средний',
            'origin': 'Россия',
            'founded_year': 1993,
            'key_products': 'Облачная телефония, видеоконференцсвязь, контакт-центр',
            'target_customers': 'Государственный сектор, крупный бизнес, SMB',
            'advantages': 'Российская разработка, соответствие требованиям законодательства',
            'software_registry': 'Да',
            'fstek': 'Да',
            'fsb': 'Да',
            'main_competitors': 'МТС, МегаФон, Tele2',
            'certified_engineers': 'Да',
            'warehouse_availability': 'Нет',
            'service_provided': 'Да'
        }
    ]
    
    print("Добавляем примеры вендоров в базу данных...")
    
    for vendor_data in sample_vendors:
        try:
            vendor = db.add_vendor(**vendor_data)
            print(f"✅ Добавлен вендор: {vendor.name} ({vendor.direction})")
        except Exception as e:
            print(f"❌ Ошибка при добавлении {vendor_data['name']}: {e}")
    
    print(f"\nГотово! Добавлено {len(sample_vendors)} вендоров.")
    print("Теперь можно тестировать поиск и просмотр по направлениям.")

if __name__ == '__main__':
    add_sample_vendors()