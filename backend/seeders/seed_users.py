from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from models.models import User, RoleEnum
from models import db

def seed_users():
    users = [
        {
            "email": "23f3001470@ds.study.iitm.ac.in",
            "name": "Admin",
            "phone": "9876543210",
            "role": RoleEnum.ADMIN,
            "password": "password",
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
        try:
            existing = User.query.filter_by(email=user_data["email"]).first()
            if existing:
                existing.name = user_data["name"]
                existing.phone = user_data["phone"]
                existing.role = user_data["role"]
                existing.password_hash = generate_password_hash(user_data["password"])
                existing.is_active = True
                db.session.commit()
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
                db.session.commit()
        except IntegrityError:
            db.session.rollback()
