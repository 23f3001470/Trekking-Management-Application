import random
from datetime import datetime, timedelta, date
from app import app
from models import db
from models.models import User, Trek, Booking, RoleEnum, DifficultyEnum, TrekStatusEnum, BookingStatusEnum, PaymentStatusEnum

def seed_db():
    db.drop_all()
    db.create_all()

    admin = User(
        email="23f3001470@ds.study.iitm.ac.in",
        name="Admin",
        role=RoleEnum.ADMIN,
        is_active=True
    )
    admin.set_password("password")
    db.session.add(admin)

    staff_members = []
    special_staff = User(email="georgian3499@gmail.com", name="Georgian Staff", role=RoleEnum.STAFF, is_active=True)
    special_staff.set_password("password")
    staff_members.append(special_staff)
    db.session.add(special_staff)

    for i in range(25):
        s = User(email=f"staff{i}@example.com", name=f"Staff {i}", role=RoleEnum.STAFF, is_active=True)
        s.set_password("password")
        staff_members.append(s)
        db.session.add(s)

    users = []
    special_user = User(email="dksingh01011970@gmail.com", name="DK Singh", role=RoleEnum.USER, is_active=True)
    special_user.set_password("password")
    users.append(special_user)
    db.session.add(special_user)

    for i in range(55):
        u = User(email=f"user{i}@example.com", name=f"User {i}", role=RoleEnum.USER, is_active=True)
        u.set_password("password")
        users.append(u)
        db.session.add(u)

    db.session.commit()

    treks = []
    locations = ["Himalayas", "Western Ghats", "Alps", "Rocky Mountains", "Andes"]
    difficulties = list(DifficultyEnum)
    statuses = list(TrekStatusEnum)

    for i in range(30):
        start_dt = date.today() + timedelta(days=random.randint(-100, 100))
        end_dt = start_dt + timedelta(days=random.randint(1, 10))
        
        status = random.choice(statuses)
        if end_dt < date.today() and status == TrekStatusEnum.OPEN:
            status = TrekStatusEnum.COMPLETED

        t = Trek(
            name=f"Trek {i} Adventure",
            location=random.choice(locations),
            difficulty=random.choice(difficulties),
            duration_days=(end_dt - start_dt).days,
            available_slots=random.randint(10, 50),
            assigned_staff_id=random.choice(staff_members).id,
            status=status,
            start_date=start_dt,
            end_date=end_dt,
            description="A great trekking experience."
        )
        treks.append(t)
        db.session.add(t)

    db.session.commit()

    for u in users:
        for _ in range(random.randint(1, 4)):
            t = random.choice(treks)
            b = Booking(
                user_id=u.id,
                trek_id=t.id,
                booking_date=datetime.now() - timedelta(days=random.randint(1, 30)),
                status=random.choice(list(BookingStatusEnum)),
                payment_status=random.choice(list(PaymentStatusEnum))
            )
            existing = Booking.query.filter_by(user_id=u.id, trek_id=t.id).first()
            if not existing:
                db.session.add(b)

    db.session.commit()
    print("Database seeded successfully!")

if __name__ == "__main__":
    with app.app_context():
        seed_db()
