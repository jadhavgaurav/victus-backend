
import os
import sys
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

# Add backend to path to import models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.user import User

DATABASE_URL = os.environ.get("DATABASE_URL")

def create_dev_user():
    if not DATABASE_URL:
        print("DATABASE_URL not set.")
        return

    print(f"Connecting to {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        email = "dev@victus.local"
        stmt = select(User).where(User.email == email)
        user = session.execute(stmt).scalar_one_or_none()

        if user:
            print(f"User already exists: {user.id}")
        else:
            print("Creating dev user...")
            new_user = User(
                email=email,
                username="dev_user",
                full_name="Developer",
                is_active=True,
                is_verified=True
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            print(f"User created: {new_user.id}")
            
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    create_dev_user()
