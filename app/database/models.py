"""Re-export models for SQLAdmin"""
from app.models.user import User
from app.models.menu import MenuItem
from app.models.table import RestaurantTable as Table

# Try to import Order and OrderItem if they exist
try:
    from app.models.order import Order, OrderItem
except ImportError:
    Order = None
    OrderItem = None

__all__ = ['User', 'MenuItem', 'Table', 'Order', 'OrderItem']
