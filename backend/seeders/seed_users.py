from werkzeug.security import generate_password_hash

from models.models import User, RoleEnum
from models import db


def seed_users():
    users = [
        {
            "email": "admin@trekapp.com",
            "name": "Amit Sharma",
            "phone": "9876543210",
            "role": RoleEnum.ADMIN,
            "password": "Admin@123",
        },
        {
            "email": "priya.singh@trekapp.com",
            "name": "Priya Singh",
            "phone": "9123456780",
            "role": RoleEnum.STAFF,
            "password": "Staff@123",
        },
        {
            "email": "suresh.rao@trekapp.com",
            "name": "Suresh Rao",
            "phone": "9988776655",
            "role": RoleEnum.STAFF,
            "password": "Staff@123",
        },
    ]

    for user_data in users:
        existing = User.query.filter_by(email=user_data["email"]).first()
        if existing:
            existing.name = user_data["name"]
            existing.phone = user_data["phone"]
            existing.role = user_data["role"]
            existing.password_hash = generate_password_hash(user_data["password"])
            existing.is_active = True
            print(f"Updated user: {existing.email} ({existing.role.value})")
        else:
            user = User(
                email=user_data["email"],
                name=user_data["name"],
                phone=user_data["phone"],
                role=user_data["role"],
                password_hash=generate_password_hash(user_data["password"]),
                is_active=True,
            )
            db.session.add(user)
            print(f"Created user: {user.email} ({user.role.value})")

    db.session.commit()

if __name__ == "__main__":
    from app import app

    with app.app_context():
        seed_users()
