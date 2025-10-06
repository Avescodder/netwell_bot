import requests
import csv
from io import StringIO
from db import db, VendorDirection

SHEET_ID = "1dZVhfNqjS9NalZrjd3svUnz2yNngWd2QVYbuRUbQ12U"


DIRECTION_TABS = {
    "СХД": "0",
    "Сервера": "0",
    "ИБ": "1402009523",
    "Инженерная инфраструктура": "522772291",
    "Сети": "832184783",
    "Унифицированные коммуникации": "228991952",
}

def parse_direction_tab(direction_name, gid):
    """Парсит вкладку направления"""
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
            
            vendor_data = {
                'direction': direction_name,
                'vendor_name': vendor_name,
                'description': row[1].strip() if len(row) > 1 else None,
                'origin': row[2].strip() if len(row) > 2 else None,
                'categories': row[3].strip() if len(row) > 3 else None,
                'key_products': row[4].strip() if len(row) > 4 else None,
                'advantages': row[5].strip() if len(row) > 5 else None,
                'registries': row[6].strip() if len(row) > 6 else None,
            }
            
            vendors.append(vendor_data)
        
        return vendors
        
    except Exception as e:
        print(f"  ❌ Ошибка при парсинге '{direction_name}': {e}")
        return []

def import_vendor_directions():
    print("📥 Загружаем направления из Google Sheets...\n")
    
    
    total_added = 0
    total_updated = 0
    
    for direction, gid in DIRECTION_TABS.items():
        print(f"📂 Обрабатываем: {direction}")
        vendors = parse_direction_tab(direction, gid)
        
        if not vendors:
            print(f"  ⚠️  Нет данных\n")
            continue
        
        print(f"  Найдено: {len(vendors)}")
        
        added = 0
        updated = 0
        
        for vendor_data in vendors:
            try:
                existing = db.session.query(VendorDirection).filter_by(
                    direction=direction,
                    vendor_name=vendor_data['vendor_name']
                ).first()
                
                db.add_vendor_direction(**vendor_data)
                
                if existing:
                    updated += 1
                else:
                    added += 1
                    
            except Exception as e:
                print(f"  ❌ {vendor_data['vendor_name']}: {e}")
                db.session.rollback()
        
        print(f"  ✅ Добавлено: {added}, 🔄 Обновлено: {updated}\n")
        
        total_added += added
        total_updated += updated
    
    print(f"{'='*50}")
    print(f"🎉 ИТОГО:")
    print(f"✅ Добавлено: {total_added}")
    print(f"🔄 Обновлено: {total_updated}")
    print(f"{'='*50}")

if __name__ == '__main__':
    import_vendor_directions()