from datetime import date
from models.models import DifficultyEnum, TrekStatusEnum

def parse_date(value):
    if not value:
        return None
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return value

def validate_create_trek(payload):
    name = payload.get("name")
    if not name:
        return False, "Trek name is required"

    difficulty = payload.get("difficulty")
    if difficulty:
        try:
            DifficultyEnum(difficulty)
        except ValueError:
            return False, "Invalid difficulty"

    status = payload.get("status")
    if status:
        try:
            TrekStatusEnum(status)
        except ValueError:
            return False, "Invalid status"

    start_date = payload.get("start_date")
    if start_date and not parse_date(start_date):
        return False, "Invalid start_date format"

    end_date = payload.get("end_date")
    if end_date and not parse_date(end_date):
        return False, "Invalid end_date format"

    duration_days = payload.get("duration_days")
    if duration_days is not None:
        try:
            int(duration_days)
        except ValueError:
            return False, "duration_days must be an integer"

    available_slots = payload.get("available_slots")
    if available_slots is not None:
        try:
            int(available_slots)
        except ValueError:
            return False, "available_slots must be an integer"

    return True, None

def validate_update_trek(payload):
    # validate update payload
    difficulty = payload.get("difficulty")
    if difficulty:
        try:
            DifficultyEnum(difficulty)
        except ValueError:
            return False, "Invalid difficulty"

    status = payload.get("status")
    if status:
        try:
            TrekStatusEnum(status)
        except ValueError:
            return False, "Invalid status"

    start_date = payload.get("start_date")
    if start_date and not parse_date(start_date):
        return False, "Invalid start_date format"

    end_date = payload.get("end_date")
    if end_date and not parse_date(end_date):
        return False, "Invalid end_date format"

    duration_days = payload.get("duration_days")
    if duration_days is not None:
        try:
            int(duration_days)
        except ValueError:
            return False, "duration_days must be an integer"

    available_slots = payload.get("available_slots")
    if available_slots is not None:
        try:
            int(available_slots)
        except ValueError:
            return False, "available_slots must be an integer"

    return True, None

def validate_staff_assignment(payload):
    staff_id = payload.get("staff_id")
    if staff_id is None:
        return False, "staff_id is required"
    try:
        int(staff_id)
    except ValueError:
        return False, "staff_id must be an integer"
    return True, None
