from datetime import datetime, date
from enum import Enum
from sqlalchemy.dialects.sqlite import JSON
from models import db


class RoleEnum(Enum):
    ADMIN = "admin"
    STAFF = "staff"
    USER = "user"


class DifficultyEnum(Enum):
    EASY = "Easy"
    MODERATE = "Moderate"
    HARD = "Hard"


class TrekStatusEnum(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    OPEN = "Open"
    CLOSED = "Closed"
    COMPLETED = "Completed"


class BookingStatusEnum(Enum):
    BOOKED = "Booked"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"


class PaymentStatusEnum(Enum):
    PENDING = "Pending"
    PAID = "Paid"
    REFUNDED = "Refunded"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50))
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.USER)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    bookings = db.relationship("Booking", back_populates="user", cascade="all, delete-orphan")
    assigned_treks = db.relationship("Trek", back_populates="assigned_staff")

    def __repr__(self):
        return f"<User {self.email} {self.role.value}>"


class Trek(db.Model):
    __tablename__ = "treks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    difficulty = db.Column(db.Enum(DifficultyEnum), nullable=False, default=DifficultyEnum.MODERATE)
    duration_days = db.Column(db.Integer, nullable=False, default=1)
    available_slots = db.Column(db.Integer, nullable=False, default=0)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    status = db.Column(db.Enum(TrekStatusEnum), nullable=False, default=TrekStatusEnum.PENDING)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)
    metadata = db.Column(JSON)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bookings = db.relationship("Booking", back_populates="trek", cascade="all, delete-orphan")
    assigned_staff = db.relationship("User", back_populates="assigned_treks")

    def slots_remaining(self):
        booked = sum(1 for b in self.bookings if b.status == BookingStatusEnum.BOOKED)
        return max(self.available_slots - booked, 0)

    def __repr__(self):
        return f"<Trek {self.name} {self.location} {self.status.value}>"


class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Enum(BookingStatusEnum), nullable=False, default=BookingStatusEnum.BOOKED)
    payment_status = db.Column(db.Enum(PaymentStatusEnum), nullable=False, default=PaymentStatusEnum.PENDING)
    extra = db.Column(JSON)
    user = db.relationship("User", back_populates="bookings")
    trek = db.relationship("Trek", back_populates="bookings")

    __table_args__ = (db.UniqueConstraint("user_id", "trek_id", name="uix_user_trek"),)

    def __repr__(self):
        return f"<Booking user={self.user_id} trek={self.trek_id} status={self.status.value}>"
