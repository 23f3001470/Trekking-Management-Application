import re
from models.models import BookingStatusEnum

def validate_profile_update(payload):
    name = payload.get("name")
    if name is not None and not name.strip():
        return False, "Name cannot be empty if provided"
        
    password = payload.get("password")
    if password is not None and len(password) < 6:
        return False, "Password must be at least 6 characters long"

    phone = payload.get("phone")
    if phone is not None:
        # basic phone regex
        if not re.match(r"^[\d\+\-\s()]*$", phone):
            return False, "Invalid phone number format"

    return True, None

def validate_booking_status_update(payload):
    status = payload.get("status")
    if not status:
        return False, "status is required"
    try:
        BookingStatusEnum(status)
    except ValueError:
        return False, "Invalid booking status"
    return True, None

def validate_staff_creation(payload):
    email = payload.get("email")
    name = payload.get("name")
    password = payload.get("password")

    if not email or not name or not password:
        return False, "Email, name, and password are required"
        
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Invalid email format"
        
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
        
    phone = payload.get("phone")
    if phone is not None:
        if not re.match(r"^[\d\+\-\s()]*$", phone):
            return False, "Invalid phone number format"

    return True, None
