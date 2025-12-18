"""Database migration script using Alembic"""
import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from alembic.config import Config
from alembic import command
from app.config import settings


def run_migrations(command_name='upgrade'):
    """Execute Alembic migrations"""
    
    alembic_cfg = Config('alembic.ini')
    alembic_cfg.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
    
    try:
        if command_name == 'upgrade':
            print(f'📦 Upgrading database to latest migration...')
            print(f'🗄️  Database: {settings.DATABASE_URL}')
            command.upgrade(alembic_cfg, 'head')
            print('✅ Database migrated successfully!')
            
        elif command_name == 'downgrade':
            print(f'📦 Downgrading database by 1 migration...')
            command.downgrade(alembic_cfg, '-1')
            print('✅ Database downgraded successfully!')
            
        elif command_name == 'current':
            print(f'📦 Checking current migration version...')
            command.current(alembic_cfg)
            
        elif command_name == 'history':
            print(f'📦 Migration history:')
            command.history(alembic_cfg)
            
        else:
            print(f'❌ Unknown command: {command_name}')
            print('Available commands: upgrade, downgrade, current, history')
            return False
            
        return True
        
    except Exception as e:
        print(f'❌ Migration error: {e}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    command_name = sys.argv[1] if len(sys.argv) > 1 else 'upgrade'
    success = run_migrations(command_name)
    sys.exit(0 if success else 1)
