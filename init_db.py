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
            
            # Пользователь (бывший Повар)
            user = User(
                username="userNum1",
                password_hash=pwd_context.hash("user123"),
                full_name="Алексей Сидоров",
                role="user",
                is_active=True
            )
            db.add(user)
            
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
        
        # Создаём расширенное тестовое меню
        existing_menu = db.query(MenuItem).count()
        if existing_menu > 0:
            print("⚠️  Меню уже существует, пропускаем создание...")
        else:
            print("🍽️  Создание расширенного меню...")
            
            menu_items = [
                # ЗАКУСКИ (Appetizers)
                MenuItem(
                    name="Салат Цезарь",
                    description="Классический салат с курицей, пармезаном и соусом Цезарь",
                    price=450.00,
                    category="Закуски",
                    is_available=True
                ),
                MenuItem(
                    name="Крем-суп из грибов",
                    description="Нежный суп из белых грибов со сливками и гренками",
                    price=320.00,
                    category="Закуски",
                    is_available=True
                ),
                MenuItem(
                    name="Брускетта с помидорами",
                    description="Хрустящий хлеб с помидорами, чесноком и оливковым маслом",
                    price=280.00,
                    category="Закуски",
                    is_available=True
                ),
                MenuItem(
                    name="Крем-суп из морепродуктов",
                    description="Благородный суп с креветками, кальмарами и сливками",
                    price=420.00,
                    category="Закуски",
                    is_available=True
                ),
                MenuItem(
                    name="Капрезе",
                    description="Слои моцареллы, томата и базилика с оливковым маслом",
                    price=380.00,
                    category="Закуски",
                    is_available=True
                ),
                
                # ОСНОВНЫЕ БЛЮДА (Main Courses)
                MenuItem(
                    name="Стейк из говядины",
                    description="Мраморная говядина, приготовленная на гриле, с овощами",
                    price=1200.00,
                    category="Основные блюда",
                    is_available=True
                ),
                MenuItem(
                    name="Паста Болонье",
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
                    name="Паста Карбонара",
                    description="Классическая паста со сливочным соусом и беконом",
                    price=620.00,
                    category="Основные блюда",
                    is_available=True
                ),
                MenuItem(
                    name="Курица в сливочном соусе",
                    description="Нежная куриная грудка с грибами и сливочным соусом",
                    price=580.00,
                    category="Основные блюда",
                    is_available=True
                ),
                MenuItem(
                    name="Ризотто с грибами",
                    description="Кремовое ризотто с белыми грибами и пармезаном",
                    price=520.00,
                    category="Основные блюда",
                    is_available=True
                ),
                MenuItem(
                    name="Плов по-узбекски",
                    description="Ароматный плов с мясом и овощами",
                    price=480.00,
                    category="Основные блюда",
                    is_available=True
                ),
                MenuItem(
                    name="Креветки по-тайски",
                    description="Креветки в остром соусе с лемонграссом",
                    price=780.00,
                    category="Основные блюда",
                    is_available=True
                ),
                
                # СУПЫ (Soups)
                MenuItem(
                    name="Суп Том Ям",
                    description="Острый тайский суп с морепродуктами",
                    price=350.00,
                    category="Супы",
                    is_available=True
                ),
                MenuItem(
                    name="Борщ украинский",
                    description="Традиционный борщ со сметаной",
                    price=280.00,
                    category="Супы",
                    is_available=True
                ),
                MenuItem(
                    name="Тtonкацу жидкий",
                    description="Японский суп с лапшой и свининой",
                    price=420.00,
                    category="Супы",
                    is_available=True
                ),
                
                # ДЕСЕРТЫ (Desserts)
                MenuItem(
                    name="Шоколадный мусс",
                    description="Нежный шоколадный мусс с ягодами",
                    price=280.00,
                    category="Десерты",
                    is_available=True
                ),
                MenuItem(
                    name="Тирамису",
                    description="Классический итальянский десерт с маскарпоне",
                    price=320.00,
                    category="Десерты",
                    is_available=True
                ),
                MenuItem(
                    name="Панна-котта",
                    description="Нежный сливочный десерт с ягодным соусом",
                    price=300.00,
                    category="Десерты",
                    is_available=True
                ),
                MenuItem(
                    name="Чизкейк",
                    description="Нью-йоркский чизкейк с клубничным джемом",
                    price=350.00,
                    category="Десерты",
                    is_available=True
                ),
                MenuItem(
                    name="Профитроли",
                    description="Заварные пирожные с шоколадным соусом",
                    price=270.00,
                    category="Десерты",
                    is_available=True
                ),
                MenuItem(
                    name="Брауни",
                    description="Шоколадный брауни с орехами",
                    price=260.00,
                    category="Десерты",
                    is_available=True
                ),
                
                # НАПИТКИ (Beverages)
                MenuItem(
                    name="Эспрессо",
                    description="Крепкий итальянский кофе",
                    price=120.00,
                    category="Напитки",
                    is_available=True
                ),
                MenuItem(
                    name="Капучино",
                    description="Кофе с молочной пеной",
                    price=150.00,
                    category="Напитки",
                    is_available=True
                ),
                MenuItem(
                    name="Латте",
                    description="Кофе с горячим молоком",
                    price=160.00,
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
                MenuItem(
                    name="Апельсиновый фреш",
                    description="Свежевыжатый апельсиновый сок",
                    price=180.00,
                    category="Напитки",
                    is_available=True
                ),
                MenuItem(
                    name="Лимонад",
                    description="Домашний лимонад с лимоном и мятой",
                    price=140.00,
                    category="Напитки",
                    is_available=True
                ),
                MenuItem(
                    name="Красное вино",
                    description="Красное вино (бокал 150мл)",
                    price=250.00,
                    category="Напитки",
                    is_available=True
                ),
                MenuItem(
                    name="Белое вино",
                    description="Белое вино (бокал 150мл)",
                    price=250.00,
                    category="Напитки",
                    is_available=True
                ),
                MenuItem(
                    name="Пиво",
                    description="Холодное пиво (0.5л)",
                    price=200.00,
                    category="Напитки",
                    is_available=True
                ),
            ]
            
            for item in menu_items:
                db.add(item)
            
            db.commit()
            print(f"✅ Меню создано! Добавлено {len(menu_items)} блюд")
        
        # Создаём тестовые столы
        existing_tables = db.query(RestaurantTable).count()
        if existing_tables > 0:
            print("⚠️  Столы уже существуют, пропускаем создание...")
        else:
            print("🪑 Создание тестовых столов...")
            
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
        print("\n📋 Новые данные для входа:")
        print("👔 Официант: ofikNum1 / waiter123")
        print("👤 Пользователь: userNum1 / user123")
        print("🧑‍💼 Администратор: adminNum1 / admin123")
        
    except Exception as e:
        print(f"❌ Ошибка при инициализации БД: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
