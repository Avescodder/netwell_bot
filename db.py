"""
Модель данных и работа с базой данных
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
from config import DATABASE_URL

Base = declarative_base()

class User(Base):
    """Таблица пользователей"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)  
    username = Column(String(50), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    full_name = Column(String(200), nullable=True)  
    company = Column(String(200), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        """Преобразование объекта в словарь"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'full_name': self.full_name,
            'company': self.company,
            'phone': self.phone,
            'email': self.email,
            'registration_date': self.registration_date.isoformat() if self.registration_date else None
        }

class Vendor(Base):
    """Таблица вендоров"""
    __tablename__ = 'vendors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    priority = Column(String(50), nullable=True) 
    origin = Column(String(100), nullable=True) 
    founded_year = Column(Integer, nullable=True)  
    categories = Column(Text, nullable=True)  
    key_products = Column(Text, nullable=True)  
    target_customers = Column(Text, nullable=True) 
    advantages = Column(Text, nullable=True)  
    software_registry = Column(String(10), nullable=True)  
    fstek = Column(String(10), nullable=True)  
    fsb = Column(String(10), nullable=True) 
    decision_makers = Column(Text, nullable=True)  
    main_competitors = Column(Text, nullable=True)  
    foreign_replacement = Column(Text, nullable=True)  
    service = Column(Text, nullable=True)  
    partner_program = Column(Text, nullable=True)  
    partner_requirements = Column(Text, nullable=True)  
    partner_benefits = Column(Text, nullable=True)  
    sales_recommendations = Column(Text, nullable=True)  
    certified_engineers = Column(String(10), nullable=True)  
    warehouse_availability = Column(String(10), nullable=True)  
    service_provided = Column(String(10), nullable=True)  
    direction = Column(String(100), nullable=True)  
    description = Column(Text, nullable=True)  
    vendor_on_our_site = Column(String(10), nullable=True)
    netwell_on_vendor_site = Column(String(10), nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    
    def to_card_text(self):
        """Форматирование карточки вендора для отображения"""
        card = f"🏢 **{self.name}**\n"
        card += "━━━━━━━━━━━━━━━━━━\n\n"
        
        if self.priority:
            card += f"⭐ **Приоритет:** {self.priority}\n\n"
        
        if self.origin:
            card += f"🌍 **Происхождение:** {self.origin}\n"
        if self.founded_year:
            card += f"📅 **Год основания:** {self.founded_year}\n"
        
        if self.categories:
            card += f"\n📦 **Категории продуктов:**\n"
            categories_list = [cat.strip() for cat in self.categories.split('\n') if cat.strip()]
            for cat in categories_list[:5]:  # максимум 5 категорий
                card += f"  • {cat}\n"
        
        if self.key_products:
            card += f"\n🔑 **Ключевые продукты:**\n"
            products_list = [prod.strip() for prod in self.key_products.split('\n') if prod.strip()]
            for prod in products_list[:5]:  # максимум 5 продуктов
                card += f"  • {prod}\n"
        
        if self.target_customers:
            card += f"\n👥 **Целевые клиенты:**\n"
            customers_list = [cust.strip() for cust in self.target_customers.split('\n') if cust.strip()]
            for cust in customers_list[:5]:  # максимум 5 пунктов
                card += f"  • {cust}\n"
        
        if self.advantages:
            card += f"\n⭐ **Преимущества:**\n"
            advantages_list = [adv.strip() for adv in self.advantages.split('\n') if adv.strip()]
            for adv in advantages_list[:5]:
                card += f"  • {adv}\n"
        
        registries = []
        if self.software_registry and 'да' in self.software_registry.lower():
            registries.append('Реестр ПО')
        if self.fstek and 'да' in self.fstek.lower():
            registries.append('ФСТЭК')
        if self.fsb and 'да' in self.fsb.lower():
            registries.append('ФСБ')
        if registries:
            card += f"\n📋 **Сертификации:** {', '.join(registries)}\n"
        
        if self.main_competitors:
            competitors_list = [comp.strip() for comp in self.main_competitors.split('\n') if comp.strip()]
            if len(competitors_list) > 1:
                card += f"\n🥊 **Конкуренты:** {', '.join(competitors_list[:3])}\n"
            else:
                card += f"\n🥊 **Конкуренты:** {self.main_competitors}\n"
        
        indicators = []
        if self.certified_engineers and 'да' in str(self.certified_engineers).lower():
            indicators.append('✅ Инженеры')
        if self.warehouse_availability and 'да' in str(self.warehouse_availability).lower():
            indicators.append('✅ Склад')
        if self.service_provided and 'да' in str(self.service_provided).lower():
            indicators.append('✅ Сервис')
        
        if indicators:
            card += f"\n{'  '.join(indicators)}\n"
        
        if self.partner_program:
            card += f"\n🤝 **Партнерская программа:**\n{self.partner_program[:200]}\n"
        
        if self.sales_recommendations:
            card += f"\n💡 **Рекомендации по продажам:**\n{self.sales_recommendations[:200]}\n"
        
        return card

class UserLog(Base):
    """Таблица логов действий пользователей"""
    __tablename__ = 'user_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)  
    action = Column(String(100), nullable=False)  
    details = Column(Text, nullable=True)  
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'details': self.details,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }


class VendorDirection(Base):
    """Таблица вендоров по направлениям (для раздела "Изучить направления")"""
    __tablename__ = 'vendor_directions'
    
    id = Column(Integer, primary_key=True)
    direction = Column(String(100), nullable=False)  
    vendor_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)  
    origin = Column(String(100), nullable=True)  
    categories = Column(Text, nullable=True)  
    key_products = Column(Text, nullable=True) 
    advantages = Column(Text, nullable=True) 
    registries = Column(Text, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    
    def to_card_text(self):
        """Форматирование карточки для направления"""
        card = f"🏢 **{self.vendor_name}**\n"
        card += "━━━━━━━━━━━━━━━━━━\n\n"
        
        if self.description:
            card += f"{self.description}\n\n"
        
        if self.origin:
            card += f"🌍 **Происхождение:** {self.origin}\n\n"
        
        if self.categories:
            card += f"📦 **Категории продуктов:**\n"
            categories_list = [cat.strip() for cat in self.categories.split('\n') if cat.strip()]
            for cat in categories_list[:5]:
                card += f"  • {cat}\n"
            card += "\n"
        
        if self.key_products:
            card += f"🔑 **Ключевые продукты:**\n"
            products_list = [prod.strip() for prod in self.key_products.split('\n') if prod.strip()]
            for prod in products_list[:5]:
                card += f"  • {prod}\n"
            card += "\n"
        
        if self.advantages:
            card += f"⭐ **Конкурентные преимущества:**\n"
            advantages_list = [adv.strip() for adv in self.advantages.split('\n') if adv.strip()]
            for adv in advantages_list[:5]:
                card += f"  • {adv}\n"
            card += "\n"
        
        if self.registries:
            card += f"📋 **Сертификации:** {self.registries}\n"
        
        return card
class DatabaseManager:
    """Менеджер для работы с базой данных"""
    
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        """Добавление нового пользователя"""
        user = self.session.query(User).filter_by(user_id=user_id).first()
        if not user:
            user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            self.session.add(user)
            self.session.commit()
        return user
    
    def update_user_profile(self, user_id: int, **kwargs):
        """Обновление профиля пользователя"""
        user = self.session.query(User).filter_by(user_id=user_id).first()
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self.session.commit()
            return user
        return None
    
    def get_user(self, user_id: int):
        """Получение пользователя по ID"""
        return self.session.query(User).filter_by(user_id=user_id).first()
    
    def get_all_users(self):
        """Получение всех пользователей"""
        return self.session.query(User).all()
    
    def add_vendor(self, **vendor_data):
        """Добавление или обновление вендора"""
        vendor = self.session.query(Vendor).filter_by(name=vendor_data['name']).first()
        if vendor:
            for key, value in vendor_data.items():
                if hasattr(vendor, key):
                    setattr(vendor, key, value)
        else:
            vendor = Vendor(**vendor_data)
            self.session.add(vendor)
        
        self.session.commit()
        return vendor
    
    def get_vendors_by_direction_flexible(self, direction: str):
        """Получение вендоров по направлению (гибкий поиск в categories)"""
        vendors = self.session.query(Vendor).filter(
            (Vendor.direction == direction) | 
            (Vendor.categories.like(f'%{direction}%'))
        ).all()
        return vendors
    
    def get_vendor(self, name: str):
        """Поиск вендора по названию"""
        return self.session.query(Vendor).filter(Vendor.name.ilike(f'%{name}%')).first()
    
    def get_vendors_by_direction(self, direction: str):
        """Получение вендоров по направлению"""
        return self.session.query(Vendor).filter_by(direction=direction).all()
    
    def get_vendor_by_id(self, id: int):
        """Получение вендоров по id"""
        return self.session.query(Vendor).filter_by(id=id).first()

    def get_all_vendors(self):
        """Получение всех вендоров"""
        return self.session.query(Vendor).all()
    
    def log_user_action(self, user_id: int, action: str, details: str = None):
        """Логирование действий пользователя"""
        log = UserLog(user_id=user_id, action=action, details=details)
        self.session.add(log)
        self.session.commit()
    
    def get_user_stats(self):
        """Получение статистики пользователей"""
        total_users = self.session.query(User).count()
        active_users = self.session.query(User).filter_by(is_active=True).count()
        
        from datetime import timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_logs = self.session.query(UserLog).filter(UserLog.timestamp >= week_ago).all()
        
        action_counts = {}
        for log in recent_logs:
            action_counts[log.action] = action_counts.get(log.action, 0) + 1
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'popular_actions': action_counts
        }

    def add_vendor_direction(self, **data):
        """Добавление или обновление вендора по направлению"""
        vendor_dir = self.session.query(VendorDirection).filter_by(
            direction=data['direction'],
            vendor_name=data['vendor_name']
        ).first()
        
        if vendor_dir:
            for key, value in data.items():
                if hasattr(vendor_dir, key):
                    setattr(vendor_dir, key, value)
        else:
            vendor_dir = VendorDirection(**data)
            self.session.add(vendor_dir)
        
        self.session.commit()
        return vendor_dir

    def get_vendors_by_direction_new(self, direction: str):
        """Получение вендоров по направлению из новой таблицы"""
        return self.session.query(VendorDirection).filter_by(direction=direction).all()

    def clear_vendor_directions(self):
        """Очистка таблицы направлений (для полной перезагрузки)"""
        self.session.query(VendorDirection).delete()
        self.session.commit()
    
    def close(self):
        """Закрытие соединения с базой данных"""
        self.session.close()

db = DatabaseManager()

