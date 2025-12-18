#!/usr/bin/env python
"""
Simplified script to reset database - run from project root
Usage: python reset_database.py
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

# Import models
from app.database.core import Base, SQLALCHEMY_DATABASE_URL
from app.models.user import User
from app.models.menu import MenuItem
from app.models.table import RestaurantTable
from app.models.order import Order


def enable_foreign_keys(dbapi_connection, connection_record):
    """Enable foreign key constraints for SQLite"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def reset_database():
    """
    Complete database reset:
    1. Drop all tables
    2. Recreate with proper constraints
    3. Create default users
    """
    
    # Create engine with foreign keys enabled
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
    
    # Enable foreign key constraints
    event.listen(Engine, "connect", enable_foreign_keys)
    
    print("\n" + "="*60)
    print("🔄 RESETTING DATABASE")
    print("="*60)
    
    # Drop all tables
    print("\n🗑️  Dropping all existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("   ✅ Tables dropped")
    
    # Create all tables with new schema
    print("\n✅ Creating all tables with constraints...")
    Base.metadata.create_all(bind=engine)
    print("   ✅ Tables created")
    
    # Create default users
    print("\n👥 Creating default users...")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Create default users
        users_data = [
            {
                "username": "chefNum1",
                "password": "chef123",
                "full_name": "Иван Шеф",
                "role": "chef"
            },
            {
                "username": "waiterNum1",
                "password": "waiter123",
                "full_name": "Петр Официант",
                "role": "waiter"
            },
            {
                "username": "adminNum1",
                "password": "admin123",
                "full_name": "Иван Админ",
                "role": "admin"
            }
        ]
        
        for user_data in users_data:
            user = User(**user_data)
            db.add(user)
            print(f"   ✅ Created user: {user_data['username']} ({user_data['role']})")
        
        db.commit()
        
        # Create default tables
        print("\n🍽️  Creating default restaurant tables...")
        for table_num in range(1, 6):
            table = RestaurantTable(table_number=table_num, seats=4, is_occupied=False)
            db.add(table)
            print(f"   ✅ Created table: {table_num}")
        
        db.commit()
        
        # Create default menu items
        print("\n🍽️  Creating default menu items...")
        menu_items_data = [
            {"name": "Борщ", "description": "Украинский борщ", "price": 250.0, "category": "Супы"},
            {"name": "Мясной стейк", "description": "Ароматный стейк", "price": 750.0, "category": "Основные"},
            {"name": "Салат Цезарь", "description": "Классический салат", "price": 300.0, "category": "Салаты"},
            {"name": "Компот", "description": "Фруктовый компот", "price": 100.0, "category": "Напитки"},
            {"name": "Чизкейк", "description": "Нью-йоркский чизкейк", "price": 200.0, "category": "Десерты"},
        ]
        
        for item_data in menu_items_data:
            item = MenuItem(**item_data)
            db.add(item)
            print(f"   ✅ Created menu item: {item_data['name']}")
        
        db.commit()
        db.close()
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating default data: {str(e)}")
        raise
    
    print("\n" + "="*60)
    print("✅ DATABASE RESET COMPLETE!")
    print("="*60)
    print("\n🔑 Default users:")
    print("   Повар: chefNum1 / chef123")
    print("   Официант: waiterNum1 / waiter123")
    print("   Администратор: adminNum1 / admin123")
    print("\n✨ All buttons should now work correctly!\n")


if __name__ == "__main__":
    reset_database()
