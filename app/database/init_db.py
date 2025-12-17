from app.database.core import SessionLocal, Base, engine
from app.models.user import User
from app.models.menu import MenuItem
from app.models.table import Table
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    """Initialize database with tables and test data"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("✅ Database already initialized with users")
            return
        
        print("🔧 Initializing database...")
        
        # Create test users
        users = [
            User(
                username="chefNum1",
                password_hash=pwd_context.hash("chef123"),
                full_name="Иван Повар",
                role="chef"
            ),
            User(
                username="waiterNum1",
                password_hash=pwd_context.hash("waiter123"),
                full_name="Петр Официант",
                role="waiter"
            ),
            User(
                username="adminNum1",
                password_hash=pwd_context.hash("admin123"),
                full_name="Сергей Админ",
                role="admin"
            )
        ]
        
        db.add_all(users)
        db.commit()
        print("✅ Test users created:")
        print("   👨‍🍳 Повар: chefNum1 / chef123")
        print("   👔 Официант: waiterNum1 / waiter123")
        print("   👨‍💼 Админ: adminNum1 / admin123")
        
        # Create test menu items
        menu_items = [
            MenuItem(name="Борщ", description="Украинский борщ со сметаной", price=150.0, category="Блюда"),
            MenuItem(name="Пельмени", description="Домашние пельмени с маслом", price=200.0, category="Блюда"),
            MenuItem(name="Салат Цезарь", description="Классический салат с курицей", price=250.0, category="Салаты"),
            MenuItem(name="Кофе", description="Эспрессо", price=80.0, category="Напитки"),
            MenuItem(name="Пиво", description="Холодное пиво", price=120.0, category="Напитки"),
            MenuItem(name="Тирамису", description="Итальянский десерт", price=180.0, category="Десерты"),
        ]
        
        db.add_all(menu_items)
        db.commit()
        print("✅ Menu items created (6 items)")
        
        # Create test tables
        tables = [
            Table(table_number=1, seats=2),
            Table(table_number=2, seats=2),
            Table(table_number=3, seats=4),
            Table(table_number=4, seats=4),
            Table(table_number=5, seats=6),
            Table(table_number=6, seats=6),
        ]
        
        db.add_all(tables)
        db.commit()
        print("✅ Restaurant tables created (6 tables)")
        
        print("\n🎉 Database initialization complete!\n")
        
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
