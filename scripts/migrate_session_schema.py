import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from src.config import settings

def migrate():
    print(f"Migrating database at {settings.DATABASE_URL}")
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        # Check if columns exist (SQLite specific logic or generic)
        # Using simple ALTER TABLE. SQLite supports ADD COLUMN.
        
        try:
            conn.execute(text("ALTER TABLE sessions ADD COLUMN expires_at TIMESTAMP WITH TIME ZONE;"))
            print("Added expires_at column.")
        except Exception as e:
            print(f"Skipping expires_at (maybe exists): {e}")
            
        try:
            conn.execute(text("ALTER TABLE sessions ADD COLUMN revoked_at TIMESTAMP WITH TIME ZONE;"))
            print("Added revoked_at column.")
        except Exception as e:
            print(f"Skipping revoked_at (maybe exists): {e}")

        conn.commit()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
