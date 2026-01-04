import sys
import os
from sqlalchemy import text

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import SessionLocal

def migrate():
    db = SessionLocal()
    try:
        print("Attempting to add 'is_superuser' column to 'users' table...")
        # Postgres-specific syntax (psycopg2 used in error log)
        db.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_superuser BOOLEAN DEFAULT FALSE;"))
        db.commit()
        print("Migration successful.")
    except Exception as e:
        print(f"Migration error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
