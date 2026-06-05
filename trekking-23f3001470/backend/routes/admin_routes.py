from datetime import date

from flask import Blueprint, g, jsonify, request

from models import db
from models.models import Booking, DifficultyEnum, RoleEnum, Trek, TrekStatusEnum, User
from routes.auth_routes import roles_required, token_auth_required, user_to_dict

bp = Blueprint("admin", __name__)


def get_request_data():
    """Extract data from JSON or form-data."""
    if request.is_json:
        return request.get_json() or {}
    return request.form.to_dict() or {}


def parse_date(value):
    if not value:
        return None
    if isinstance(value, str):
        return date.fromisoformat(value)
    return value


def trek_to_dict(trek):
    return {
        "id": trek.id,
        "name": trek.name,
        "location": trek.location,
        "difficulty": trek.difficulty.value if trek.difficulty else None,
        "duration_days": trek.duration_days,
        "available_slots": trek.available_slots,
        "assigned_staff": user_to_dict(trek.assigned_staff) if trek.assigned_staff else None,
        "status": trek.status.value if trek.status else None,
        "start_date": trek.start_date.isoformat() if trek.start_date else None,
        "end_date": trek.end_date.isoformat() if trek.end_date else None,
        "description": trek.description,
        "metadata": trek.trek_metadata,
        "created_at": trek.created_at.isoformat() if trek.created_at else None,
        "slots_remaining": trek.slots_remaining(),
    }


def booking_to_dict(booking):
    return {
        "id": booking.id,
        "user": user_to_dict(booking.user) if booking.user else None,
        "trek": trek_to_dict(booking.trek) if booking.trek else None,
        "booking_date": booking.booking_date.isoformat() if booking.booking_date else None,
        "status": booking.status.value if booking.status else None,
        "payment_status": booking.payment_status.value if booking.payment_status else None,
        "extra": booking.extra,
    }


@bp.route("/dashboard", methods=["GET"])
@token_auth_required
@roles_required(RoleEnum.ADMIN)
def dashboard():
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role=RoleEnum.USER).count()
    total_staff = User.query.filter_by(role=RoleEnum.STAFF).count()
    total_bookings = Booking.query.count()
    return jsonify(
        {
            "total_treks": total_treks,
            "total_users": total_users,
            "total_staff": total_staff,
            "total_bookings": total_bookings,
        }
    )


@bp.route("/treks", methods=["GET"])
@token_auth_required
@roles_required(RoleEnum.ADMIN)
def list_treks():
    treks = Trek.query.order_by(Trek.id.desc()).all()
    return jsonify({"treks": [trek_to_dict(t) for t in treks]})


@bp.route("/treks", methods=["POST"])
@token_auth_required
@roles_required(RoleEnum.ADMIN)
def create_trek():
    payload = get_request_data()
    name = payload.get("name")
    if not name:
        return jsonify({"error": "Trek name is required"}), 400

    difficulty = payload.get("difficulty")
    duration_days = payload.get("duration_days", 1)
    available_slots = payload.get("available_slots", 0)
    status = payload.get("status", TrekStatusEnum.PENDING.value)
    start_date = parse_date(payload.get("start_date"))
    end_date = parse_date(payload.get("end_date"))

    trek = Trek(
        name=name,
        location=payload.get("location"),
        difficulty=DifficultyEnum(difficulty) if difficulty else DifficultyEnum.MODERATE,
        duration_days=duration_days,
        available_slots=available_slots,
        status=TrekStatusEnum(status) if status else TrekStatusEnum.PENDING,
        start_date=start_date,
        end_date=end_date,
        description=payload.get("description"),
        trek_metadata=payload.get("metadata"),
    )
    db.session.add(trek)
    db.session.commit()
    return jsonify({"message": "Trek created successfully", "trek": trek_to_dict(trek)}), 201


@bp.route("/treks/<int:trek_id>", methods=["PUT"])
@token_auth_required
@roles_required(RoleEnum.ADMIN)
def update_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    payload = get_request_data()
    if "name" in payload:
        trek.name = payload["name"]
    if "location" in payload:
        trek.location = payload["location"]
    if "difficulty" in payload:
        trek.difficulty = DifficultyEnum(payload["difficulty"])
    if "duration_days" in payload:
        trek.duration_days = payload["duration_days"]
    if "available_slots" in payload:
        trek.available_slots = payload["available_slots"]
    if "status" in payload:
        trek.status = TrekStatusEnum(payload["status"])
    if "start_date" in payload:
        trek.start_date = parse_date(payload["start_date"])
    if "end_date" in payload:
        trek.end_date = parse_date(payload["end_date"])
    if "description" in payload:
        trek.description = payload["description"]
    if "metadata" in payload:
        trek.trek_metadata = payload["metadata"]

    db.session.commit()
    return jsonify({"message": "Trek updated successfully", "trek": trek_to_dict(trek)})


@bp.route("/treks/<int:trek_id>", methods=["DELETE"])
@token_auth_required
@roles_required(RoleEnum.ADMIN)
def delete_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    db.session.delete(trek)
    db.session.commit()
    return jsonify({"message": "Trek deleted successfully"})


@bp.route("/staff", methods=["POST"])
@token_auth_required
@roles_required(RoleEnum.ADMIN)
def create_staff():
    payload = get_request_data()
    email = payload.get("email")
    name = payload.get("name")
    password = payload.get("password")
    if not email or not name or not password:
        return jsonify({"error": "Email, name, and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already in use"}), 400

    staff = User(
        email=email,
        name=name,
        phone=payload.get("phone"),
        role=RoleEnum.STAFF,
        is_active=True,
    )
    staff.set_password(password)
    db.session.add(staff)
    db.session.commit()
    return jsonify({"message": "Staff created successfully", "staff": user_to_dict(staff)}), 201


@bp.route("/treks/<int:trek_id>/assign_staff", methods=["PUT"])
@token_auth_required
@roles_required(RoleEnum.ADMIN)
def assign_staff(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    payload = get_request_data()
    staff_id = payload.get("staff_id")
    if staff_id is None:
        return jsonify({"error": "staff_id is required"}), 400

    staff = User.query.get(staff_id)
    if not staff or staff.role != RoleEnum.STAFF:
        return jsonify({"error": "Staff member not found"}), 404
    if not staff.is_active:
        return jsonify({"error": "Cannot assign inactive staff"}), 400

    trek.assigned_staff = staff
    db.session.commit()
    return jsonify({"message": "Staff assigned successfully", "trek": trek_to_dict(trek)})


@bp.route("/bookings", methods=["GET"])
@token_auth_required
@roles_required(RoleEnum.ADMIN)
def list_bookings():
    bookings = Booking.query.order_by(Booking.id.desc()).all()
    return jsonify({"bookings": [booking_to_dict(b) for b in bookings]})


@bp.route("/users", methods=["GET"])
@token_auth_required
@roles_required(RoleEnum.ADMIN)
def list_users():
    role = request.args.get("role")
    query = User.query
    if role == "staff":
        query = query.filter_by(role=RoleEnum.STAFF)
    elif role == "user":
        query = query.filter_by(role=RoleEnum.USER)
    elif role == "admin":
        query = query.filter_by(role=RoleEnum.ADMIN)

    users = query.order_by(User.id.desc()).all()
    return jsonify({"users": [user_to_dict(u) for u in users]})


@bp.route("/users/<int:user_id>/deactivate", methods=["PUT"])
@token_auth_required
@roles_required(RoleEnum.ADMIN)
def deactivate_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.role == RoleEnum.ADMIN:
        return jsonify({"error": "Admin accounts cannot be deactivated"}), 400

    user.is_active = False
    db.session.commit()
    return jsonify({"message": "User deactivated successfully", "user": user_to_dict(user)})


@bp.route("/users/<int:user_id>/activate", methods=["PUT"])
@token_auth_required
@roles_required(RoleEnum.ADMIN)
def activate_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.is_active = True
    db.session.commit()
    return jsonify({"message": "User activated successfully", "user": user_to_dict(user)})


@bp.route("/search/users", methods=["GET"])
@token_auth_required
@roles_required(RoleEnum.ADMIN)
def search_users():
    query_text = request.args.get("q", "").strip()
    if not query_text:
        return jsonify({"error": "Query parameter q is required"}), 400

    users = (
        User.query.filter(User.role == RoleEnum.USER)
        .filter(
            (User.name.ilike(f"%{query_text}%"))
            | (User.email.ilike(f"%{query_text}%"))
            | (User.phone.ilike(f"%{query_text}%"))
        )
        .order_by(User.id.desc())
        .all()
    )
    return jsonify({"users": [user_to_dict(u) for u in users]})


@bp.route("/search/staff", methods=["GET"])
@token_auth_required
@roles_required(RoleEnum.ADMIN)
def search_staff():
    query_text = request.args.get("q", "").strip()
    if not query_text:
        return jsonify({"error": "Query parameter q is required"}), 400

    staff = (
        User.query.filter(User.role == RoleEnum.STAFF)
        .filter(
            (User.name.ilike(f"%{query_text}%"))
            | (User.email.ilike(f"%{query_text}%"))
            | (User.phone.ilike(f"%{query_text}%"))
        )
        .order_by(User.id.desc())
        .all()
    )
    return jsonify({"staff": [user_to_dict(u) for u in staff]})


@bp.route("/search/treks", methods=["GET"])
@token_auth_required
@roles_required(RoleEnum.ADMIN)
def search_treks():
    query_text = request.args.get("q", "").strip()
    if not query_text:
        return jsonify({"error": "Query parameter q is required"}), 400

    treks = (
        Trek.query.filter(
            (Trek.name.ilike(f"%{query_text}%"))
            | (Trek.location.ilike(f"%{query_text}%"))
            | (Trek.description.ilike(f"%{query_text}%"))
        )
        .order_by(Trek.id.desc())
        .all()
    )
    return jsonify({"treks": [trek_to_dict(t) for t in treks]})
