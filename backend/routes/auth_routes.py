import os
from functools import wraps

from flask import Blueprint, current_app, g, jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer as Serializer

from models import db
from models.models import RoleEnum, User

bp = Blueprint("auth", __name__)


def get_request_data():
    """Extract data from JSON or form-data."""
    if request.is_json:
        return request.get_json() or {}
    return request.form.to_dict() or {}


def generate_auth_token(user, expires_sec=3600):
    serializer = Serializer(current_app.config["SECRET_KEY"], salt="auth-token")
    return serializer.dumps({"id": user.id})


def verify_auth_token(token, max_age=3600):
    serializer = Serializer(current_app.config["SECRET_KEY"], salt="auth-token")
    try:
        data = serializer.loads(token, max_age=max_age)
    except SignatureExpired:
        return None
    except BadSignature:
        return None

    return User.query.get(data.get("id"))


def token_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid authorization header"}), 401

        token = auth_header.split(" ", 1)[1].strip()
        user = verify_auth_token(token)
        if not user:
            return jsonify({"error": "Invalid or expired token"}), 401

        g.current_user = user
        return f(*args, **kwargs)

    return decorated


def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            current_user = getattr(g, "current_user", None)
            if not current_user:
                return jsonify({"error": "Authentication required"}), 401

            allowed_roles = [role.value if isinstance(role, RoleEnum) else role for role in roles]
            if current_user.role.value not in allowed_roles:
                return jsonify({"error": "Access denied for your role"}), 403

            return f(*args, **kwargs)

        return wrapped

    return decorator


def user_to_dict(user):
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "phone": user.phone,
        "role": user.role.value,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


@bp.route("/register", methods=["POST"])
def register():
    payload = get_request_data()
    
    from validations.auth_validators import validate_registration
    is_valid, error = validate_registration(payload)
    if not is_valid:
        return jsonify({"error": error}), 400

    email = payload.get("email")
    name = payload.get("name")
    password = payload.get("password")
    phone = payload.get("phone")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists with this email"}), 400

    user = User(
        email=email,
        name=name,
        phone=phone,
        role=RoleEnum.USER,
        is_active=True,
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = generate_auth_token(user)
    return jsonify({"message": "Registration successful", "token": token, "user": user_to_dict(user)}), 201


@bp.route("/login", methods=["POST"])
def login():
    payload = get_request_data()
    
    from validations.auth_validators import validate_login
    is_valid, error = validate_login(payload)
    if not is_valid:
        return jsonify({"error": error}), 400

    email = payload.get("email")
    password = payload.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = generate_auth_token(user)
    return jsonify({"message": "Login successful", "token": token, "user": user_to_dict(user)})


@bp.route("/me", methods=["GET"])
@token_auth_required
def me():
    return jsonify({"user": user_to_dict(g.current_user)})


@bp.route("/admin-only", methods=["GET"])
@token_auth_required
@roles_required(RoleEnum.ADMIN)
def admin_only():
    return jsonify({"message": "Admin access granted", "user": user_to_dict(g.current_user)})


@bp.route("/staff-or-admin", methods=["GET"])
@token_auth_required
@roles_required(RoleEnum.ADMIN, RoleEnum.STAFF)
def staff_or_admin():
    return jsonify({"message": "Staff/Admin access granted", "user": user_to_dict(g.current_user)})
