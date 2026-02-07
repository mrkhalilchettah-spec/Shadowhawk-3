from app.core.db import SessionLocal
from app.models.user import User, Role
from app.core import security
import uuid

def seed():
    db = SessionLocal()
    
    # Create Roles
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        admin_role = Role(name="admin", description="Full system access")
        db.add(admin_role)
    
    analyst_role = db.query(Role).filter(Role.name == "analyst").first()
    if not analyst_role:
        analyst_role = Role(name="analyst", description="Limited access for threat analysis")
        db.add(analyst_role)
    
    db.commit()
    db.refresh(admin_role)
    
    # Create Admin User
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            email="admin@shadowhawk.internal",
            hashed_password=security.get_password_hash("shadowhawk-admin-password"),
            role_id=admin_role.id,
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print("Created admin user")
    else:
        print("Admin user already exists")

    db.close()

if __name__ == "__main__":
    seed()
