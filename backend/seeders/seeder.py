import random
from datetime import datetime, timedelta, date
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    locations = ["Himalayas", "Western Ghats", "Alps", "Rocky Mountains", "Andes",
                 "Sahyadri", "Nilgiris", "Ladakh", "Manali", "Rishikesh"]
    trek_names = [
        "Summit Ridge", "Valley Crossing", "Forest Trail", "Glacier Walk",
        "River Route", "Peak Ascent", "Canyon Loop", "Highland Path",
        "Meadow Trek", "Cliff Edge", "Snow Pass", "Lake Circuit",
        "Sunset Trail", "Monsoon Trail", "Desert Walk", "Coastal Path",
        "Waterfall Route", "Cave Exploration", "Ridge Walk", "Temple Trail",
        "Night Trek", "Sunrise Hike", "Wildlife Trail", "Heritage Walk",
        "Base Camp", "Altitude Run", "Gorge Trail", "Plateau Path",
        "Bamboo Forest", "Boulder Scramble"
    ]
    difficulties = list(DifficultyEnum)

    for i in range(30):
        start_dt = date.today() + timedelta(days=random.randint(-90, 90))
        end_dt = start_dt + timedelta(days=random.randint(1, 7))
        past = end_dt < date.today()
        future = start_dt > date.today()

        # assign status based on timeline
        if past:
            status = random.choice([TrekStatusEnum.COMPLETED, TrekStatusEnum.CLOSED])
        elif future:
            status = random.choice([TrekStatusEnum.PENDING, TrekStatusEnum.APPROVED, TrekStatusEnum.OPEN])
        else:
            status = TrekStatusEnum.OPEN

        t = Trek(
            name=trek_names[i],
            location=random.choice(locations),
            difficulty=random.choice(difficulties),
            duration_days=(end_dt - start_dt).days,
            available_slots=random.randint(10, 50),
            assigned_staff_id=random.choice(staff_members).id,
            status=status,
            start_date=start_dt,
            end_date=end_dt,
            description=f"An exciting {trek_names[i].lower()} through {random.choice(locations).lower()}."
        )
        treks.append(t)
        db.session.add(t)

    db.session.commit()

    # create bookings with consistent status/payment combos
    for u in users:
        booked_trek_ids = set()
        for _ in range(random.randint(1, 4)):
            t = random.choice(treks)
            if t.id in booked_trek_ids:
                continue
            booked_trek_ids.add(t.id)

            if t.status == TrekStatusEnum.COMPLETED:
                b_status = random.choice([BookingStatusEnum.COMPLETED, BookingStatusEnum.CANCELLED])
                if b_status == BookingStatusEnum.COMPLETED:
                    p_status = PaymentStatusEnum.PAID
                else:
                    p_status = PaymentStatusEnum.REFUNDED
            elif t.status == TrekStatusEnum.CLOSED:
                b_status = random.choice([BookingStatusEnum.CANCELLED, BookingStatusEnum.BOOKED])
                p_status = PaymentStatusEnum.REFUNDED if b_status == BookingStatusEnum.CANCELLED else PaymentStatusEnum.PENDING
            elif t.status in [TrekStatusEnum.OPEN, TrekStatusEnum.APPROVED]:
                b_status = random.choice([BookingStatusEnum.BOOKED, BookingStatusEnum.CANCELLED])
                if b_status == BookingStatusEnum.CANCELLED:
                    p_status = PaymentStatusEnum.REFUNDED
                else:
                    p_status = random.choice([PaymentStatusEnum.PENDING, PaymentStatusEnum.PAID])
            else:
                b_status = BookingStatusEnum.BOOKED
                p_status = PaymentStatusEnum.PENDING

            b = Booking(
                user_id=u.id,
                trek_id=t.id,
                booking_date=datetime.now() - timedelta(days=random.randint(1, 60)),
                status=b_status,
                payment_status=p_status
            )
            db.session.add(b)

    db.session.commit()
    print("Database seeded successfully!")

if __name__ == "__main__":
    with app.app_context():
        seed_db()
