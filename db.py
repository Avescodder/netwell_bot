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
    created_date = Column(DateTime, default=datetime.utcnow)
    
    def to_card_text(self):
        """Форматирование карточки вендора для отображения"""
        card = f"🏢 **{self.name}**\n\n"
        
        if self.priority:
            card += f"📈 **Приоритет в развитии:** {self.priority}\n"
        if self.origin:
            card += f"🌍 **Происхождение:** {self.origin}\n"
        if self.founded_year:
            card += f"📅 **Год основания:** {self.founded_year}\n"
        if self.categories:
            card += f"📦 **Категории продуктов:** {self.categories}\n"
        if self.key_products:
            card += f"🔑 **Ключевые продукты:** {self.key_products}\n"
        if self.target_customers:
            card += f"👥 **Потенциальные заказчики:** {self.target_customers}\n"
        if self.advantages:
            card += f"⭐ **Конкурентные преимущества:** {self.advantages}\n"
        
        registries = []
        if self.software_registry == 'Да':
            registries.append('Реестр ПО')
        if self.fstek == 'Да':
            registries.append('ФСТЭК')
        if self.fsb == 'Да':
            registries.append('ФСБ')
        if registries:
            card += f"📋 **Включены в:** {', '.join(registries)}\n"
        
        if self.main_competitors:
            card += f"🥊 **Основные конкуренты:** {self.main_competitors}\n"
        if self.certified_engineers == 'Да':
            card += f"👨‍🔧 **Сертифицированные инженеры:** Есть\n"
        if self.warehouse_availability == 'Да':
            card += f"📦 **Оборудование на складе:** Есть\n"
        if self.service_provided == 'Да':
            card += f"🔧 **Сервисное обслуживание:** Предоставляем\n"
        
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
    
    def close(self):
        """Закрытие соединения с базой данных"""
        self.session.close()

db = DatabaseManager()

