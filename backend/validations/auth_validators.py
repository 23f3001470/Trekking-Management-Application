import re

def validate_registration(payload):
    email = payload.get("email")
    name = payload.get("name")
    password = payload.get("password")

    if not email or not name or not password:
        return False, "Email, name, and password are required"
        
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Invalid email format"
        
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
        
    return True, None

def validate_login(payload):
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password:
        return False, "Email and password are required"
        
    return True, None
