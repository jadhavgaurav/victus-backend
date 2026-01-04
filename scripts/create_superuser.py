import sys
import os

# Add parent dir to path to import src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import User

def create_superuser(email: str):
    """
    Promotes an existing user to superuser or creates one if logic allowed 
    (but simpler to just toggle existing user for now as we don't have password hashing here easily without importing service).
    Actually, let's just toggle is_superuser=True for the given email.
    """
    # Create a new session manually
    from src.database import SessionLocal
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"User with email {email} not found.")
            return

        user.is_superuser = True
        db.commit()
        db.refresh(user)
        print(f"User {email} is now a superuser.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/create_superuser.py <email>")
        sys.exit(1)
        
    email = sys.argv[1]
    create_superuser(email)
