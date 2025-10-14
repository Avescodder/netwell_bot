import requests
import csv
from io import StringIO
from db import db, Vendor
from config import TABLE_DIRECTIONS_SHEET_ID as SHEET_ID

SHEET_TABS = {
    "CХД": "0",
    "ИБ": "1402009523",
    "Инженерная инфраструктура": "522772291",
    "Сетевые решения": "832184783",
    "Унифицированные коммуникации": "228991952",
}

def parse_sheet_tab(tab_name, gid):
    """Парсит одну вкладку Google Sheets"""
    csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    
    try:
        response = requests.get(csv_url)
        response.raise_for_status()
        
        content = response.content.decode('utf-8-sig')
        data = StringIO(content)
        lines = list(csv.reader(data))
        
        if len(lines) < 2:
            return []
        
        headers = lines[0]
        data_rows = lines[1:]
        
        vendors = []
        for row in data_rows:
            if len(row) < 2: 
                continue
            
            if len(row) < len(headers):
                row.extend([''] * (len(headers) - len(row)))
            
            vendor_name = row[0].strip()
            
            if not vendor_name:
                continue
            
            row_dict = dict(zip(headers, row))
            
            vendor_data = {
                'name': vendor_name,
                'direction': tab_name,
                'priority': row_dict.get('Приоритет в развитии', '').strip() or None,
                'origin': row_dict.get('Происхождение вендора', '').strip() or None,
                'categories': row_dict.get('Категории продуктов', '').strip() or None,
                'key_products': row_dict.get('Ключевые продукты', '').strip() or None,
                'target_customers': row_dict.get('Потенциальные заказчики (сектор)', '').strip() or None,
                'advantages': row_dict.get('Конкурентные преимущества', '').strip() or None,
                'software_registry': row_dict.get('Включены ли в реестр ПО / ФСТЭК / ФСБ', '').strip() or None,
                'fstek': row_dict.get('ФСТЭК', '').strip() or None,
                'fsb': row_dict.get('ФСБ', '').strip() or None,
                'decision_makers': row_dict.get('ЛПР', '').strip() or None,
                'main_competitors': row_dict.get('Основные конкуренты', '').strip() or None,
                'foreign_replacement': row_dict.get('Замена иностранных производителей', '').strip() or None,
                'service': row_dict.get('Сервисное обслуживание', '').strip() or None,
                'partner_program': row_dict.get('Партнерская программа (если есть, ключевые условия)', '').strip() or None,
                'partner_requirements': row_dict.get('Требования к партнерам', '').strip() or None,
                'partner_benefits': row_dict.get('Преимущества для партнеров', '').strip() or None,
                'sales_recommendations': row_dict.get('Рекомендации по продажам', '').strip() or row_dict.get('Рекомендации по продажам:', '').strip() or None,
                'certified_engineers': row_dict.get('Наличие наших сертифицированных инженеров', '').strip() or None,
                'warehouse_availability': row_dict.get('Наличие оборудование на складе Нетвелл', '').strip() or None,
                'service_provided': row_dict.get('Оказываем ли сервис по вендору?', '').strip() or None,
                'vendor_on_our_site': row_dict.get('Наличие вендора у нас на сайте', '').strip() or None,
                'netwell_on_vendor_site': row_dict.get('Наличие Нетвелл на сайте вендора', '').strip() or None,
            }
            
            founded_year = row_dict.get('Год основания', '').strip()
            if founded_year:
                try:
                    vendor_data['founded_year'] = int(founded_year)
                except:
                    vendor_data['founded_year'] = None
            else:
                vendor_data['founded_year'] = None
            
            if vendor_data.get('categories'):
                vendor_data['description'] = vendor_data['categories'][:200]
            else:
                vendor_data['description'] = None
            
            vendors.append(vendor_data)
        
        return vendors
        
    except Exception as e:
        print(f"  ❌ Ошибка при парсинге вкладки '{tab_name}': {e}")
        import traceback
        traceback.print_exc()
        return []

def add_vendors_from_sheet():
    print("📥 Загружаем данные из всех вкладок Google Sheets...\n")
    
    total_added = 0
    total_updated = 0
    
    for tab_name, gid in SHEET_TABS.items():
        print(f"📂 Обрабатываем вкладку: {tab_name}")
        vendors = parse_sheet_tab(tab_name, gid)
        
        if not vendors:
            print(f"  ⚠️  Нет данных\n")
            continue
        
        print(f"  Найдено записей: {len(vendors)}")
        
        added = 0
        updated = 0
        
        for vendor_data in vendors:
            try:
                existing = db.session.query(Vendor).filter_by(name=vendor_data['name']).first()
                
                vendor = db.add_vendor(**vendor_data)
                
                if existing:
                    updated += 1
                else:
                    added += 1
                    
            except Exception as e:
                print(f"  ❌ Ошибка: {vendor_data['name']} - {e}")
                db.session.rollback()
        
        print(f"  ✅ Добавлено: {added}, 🔄 Обновлено: {updated}\n")
        
        total_added += added
        total_updated += updated
    
    print(f"{'='*50}")
    print(f"🎉 ИТОГО:")
    print(f"✅ Добавлено новых: {total_added}")
    print(f"🔄 Обновлено: {total_updated}")
    print(f"{'='*50}")

if __name__ == '__main__':
    add_vendors_from_sheet()