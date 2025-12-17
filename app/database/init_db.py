from app.database.core import SessionLocal, Base, engine
from app.models.user import User
from app.models.menu import MenuItem
from app.models.table import RestaurantTable
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
            print("[OK] Database already initialized with users")
            return
        
        print("[INIT] Initializing database...")
        
        # Create test users
        users = [
            User(
                username="chefNum1",
                password_hash=pwd_context.hash("chef123"),
                full_name="Ivan Chef",
                role="chef"
            ),
            User(
                username="waiterNum1",
                password_hash=pwd_context.hash("waiter123"),
                full_name="Petr Waiter",
                role="waiter"
            ),
            User(
                username="adminNum1",
                password_hash=pwd_context.hash("admin123"),
                full_name="Sergey Admin",
                role="admin"
            )
        ]
        
        db.add_all(users)
        db.commit()
        print("[OK] Test users created:")
        print("     Chef: chefNum1 / chef123")
        print("     Waiter: waiterNum1 / waiter123")
        print("     Admin: adminNum1 / admin123")
        
        # Create test menu items
        menu_items = [
            MenuItem(name="Borsch", description="Ukrainian soup", price=150.0, category="Main"),
            MenuItem(name="Pelmeni", description="Russian dumplings", price=200.0, category="Main"),
            MenuItem(name="Caesar Salad", description="Classic salad with chicken", price=250.0, category="Salads"),
            MenuItem(name="Coffee", description="Espresso", price=80.0, category="Drinks"),
            MenuItem(name="Beer", description="Cold beer", price=120.0, category="Drinks"),
            MenuItem(name="Tiramisu", description="Italian dessert", price=180.0, category="Desserts"),
        ]
        
        db.add_all(menu_items)
        db.commit()
        print("[OK] Menu items created (6 items)")
        
        # Create test tables
        tables = [
            RestaurantTable(table_number=1, seats=2),
            RestaurantTable(table_number=2, seats=2),
            RestaurantTable(table_number=3, seats=4),
            RestaurantTable(table_number=4, seats=4),
            RestaurantTable(table_number=5, seats=6),
            RestaurantTable(table_number=6, seats=6),
        ]
        
        db.add_all(tables)
        db.commit()
        print("[OK] Restaurant tables created (6 tables)")
        
        print("\n[SUCCESS] Database initialization complete!\n")
        
    except Exception as e:
        print(f"[ERROR] Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
