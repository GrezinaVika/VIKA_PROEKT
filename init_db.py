#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для инициализации базы данных и создания таблиц
"""

from app.database.core import Base, engine, SessionLocal
from app.models.user import User
from app.models.menu import MenuItem
from app.models.table import RestaurantTable
from app.models.order import Order
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    """Инициализация БД и создание тестовых данных"""
    print("🔧 Создание таблиц в БД...")
    
    # Создаём все таблицы используя Base.metadata
    Base.metadata.create_all(bind=engine)
    
    print("✅ Таблицы созданы успешно!")
    
    # Создаём тестовых пользователей
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли уже пользователи
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("⚠️  Пользователи уже существуют, пропускаем создание...")
        else:
            print("👤 Создание тестовых пользователей...")
            
            # Официант
            waiter = User(
                username="ofikNum1",
                password_hash=pwd_context.hash("waiter123"),
                full_name="Иван Петров",
                role="waiter",
                is_active=True
            )
            db.add(waiter)
            
            # Повар
            chef = User(
                username="povarNum1",
                password_hash=pwd_context.hash("chef123"),
                full_name="Сергей Иванов",
                role="chef",
                is_active=True
            )
            db.add(chef)
            
            # Администратор
            admin = User(
                username="adminNum1",
                password_hash=pwd_context.hash("admin123"),
                full_name="Александр Иванович",
                role="admin",
                is_active=True
            )
            db.add(admin)
            
            db.commit()
            print("✅ Пользователи созданы!")
        
        # Создаём тестовое меню
        existing_menu = db.query(MenuItem).count()
        if existing_menu > 0:
            print("⚠️  Меню уже существует, пропускаем создание...")
        else:
            print("🙴 Создание тестового меню...")
            
            menu_items = [
                MenuItem(
                    name="Салат Цезарь",
                    description="Классический салат с курицей, пармезаном и соусом Цезарь",
                    price=450.00,
                    category="Салаты",
                    is_available=True
                ),
                MenuItem(
                    name="Стейк из говядины",
                    description="Мраморная говядина, приготовленная на гриле",
                    price=1200.00,
                    category="Основные блюда",
                    is_available=True
                ),
                MenuItem(
                    name="Паста Болоньезе",
                    description="Спагетти с мясным соусом и пармезаном",
                    price=550.00,
                    category="Основные блюда",
                    is_available=True
                ),
                MenuItem(
                    name="Рыба на гриле",
                    description="Филе лосося с овощами и лимоном",
                    price=950.00,
                    category="Основные блюда",
                    is_available=True
                ),
                MenuItem(
                    name="Суп Том Ям",
                    description="Острый тайский суп с морепродуктами",
                    price=350.00,
                    category="Супы",
                    is_available=True
                ),
                MenuItem(
                    name="Шоколадный мусс",
                    description="Нежный шоколадный мусс с ягодами",
                    price=280.00,
                    category="Десерты",
                    is_available=True
                ),
                MenuItem(
                    name="Эспрессо",
                    description="Крепкий итальянский кофе",
                    price=120.00,
                    category="Напитки",
                    is_available=True
                ),
                MenuItem(
                    name="Вода минеральная",
                    description="Минеральная вода 0.5л",
                    price=80.00,
                    category="Напитки",
                    is_available=True
                ),
            ]
            
            for item in menu_items:
                db.add(item)
            
            db.commit()
            print("✅ Меню создано!")
        
        # Создаём тестовые столы
        existing_tables = db.query(RestaurantTable).count()
        if existing_tables > 0:
            print("⚠️  Столы уже существуют, пропускаем создание...")
        else:
            print("🧨 Создание тестовых столов...")
            
            tables = [
                RestaurantTable(table_number=1, seats=2, is_occupied=False),
                RestaurantTable(table_number=2, seats=2, is_occupied=False),
                RestaurantTable(table_number=3, seats=4, is_occupied=False),
                RestaurantTable(table_number=4, seats=4, is_occupied=False),
                RestaurantTable(table_number=5, seats=6, is_occupied=False),
                RestaurantTable(table_number=6, seats=6, is_occupied=False),
                RestaurantTable(table_number=7, seats=8, is_occupied=False),
                RestaurantTable(table_number=8, seats=8, is_occupied=False),
            ]
            
            for table in tables:
                db.add(table)
            
            db.commit()
            print("✅ Столы созданы!")
        
        print("\n✨ Инициализация БД завершена успешно!")
        print("\n📏 Новые данные для входа:")
        print("👤 Официант: ofikNum1 / waiter123")
        print("👨\u200d🍳 Повар: povarNum1 / chef123")
        print("🧑\u200d💼 Администратор: adminNum1 / admin123")
        
    except Exception as e:
        print(f"❌ Ошибка при инициализации БД: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
