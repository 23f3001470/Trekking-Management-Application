from flask import Blueprint, g, jsonify, request

from models import db
from models.models import Booking, BookingStatusEnum, RoleEnum, Trek, TrekStatusEnum, User
from routes.auth_routes import roles_required, token_auth_required, user_to_dict

bp = Blueprint("staff", __name__)

def get_request_data():
    if request.is_json:
        return request.get_json() or {}
    return request.form.to_dict() or {}

@bp.route("/dashboard", methods=["GET"])
@token_auth_required
@roles_required(RoleEnum.STAFF)
def dashboard():
    staff = g.current_user
    treks = Trek.query.filter_by(assigned_staff_id=staff.id).order_by(Trek.id.desc()).all()
    result = []
    for t in treks:
        registered = sum(1 for b in t.bookings if b.status == BookingStatusEnum.BOOKED)
        result.append({
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "status": t.status.value if t.status else None,
            "available_slots": t.available_slots,
            "registered_count": registered,
        })
    return jsonify({"assigned_treks": result})

@bp.route("/treks/<int:trek_id>", methods=["PUT"])
@token_auth_required
@roles_required(RoleEnum.STAFF)
def update_trek(trek_id):
    staff = g.current_user
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    if trek.assigned_staff_id != staff.id:
        return jsonify({"error": "Not authorized for this trek"}), 403
    payload = get_request_data()
    
    from validations.trek_validators import validate_update_trek
    is_valid, error = validate_update_trek(payload)
    if not is_valid:
        return jsonify({"error": error}), 400

    if "available_slots" in payload:
        trek.available_slots = int(payload.get("available_slots") or trek.available_slots)
    if "status" in payload:
        trek.status = TrekStatusEnum(payload.get("status"))
    db.session.commit()
    return jsonify({"message": "Trek updated", "trek": {"id": trek.id, "available_slots": trek.available_slots, "status": trek.status.value}})

@bp.route("/treks/<int:trek_id>/participants", methods=["GET"])
@token_auth_required
@roles_required(RoleEnum.STAFF)
def list_participants(trek_id):
    staff = g.current_user
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    if trek.assigned_staff_id != staff.id:
        return jsonify({"error": "Not authorized for this trek"}), 403
    participants = []
    for b in trek.bookings:
        participants.append({
            "booking_id": b.id,
            "user": user_to_dict(b.user) if b.user else None,
            "status": b.status.value if b.status else None,
            "payment_status": b.payment_status.value if b.payment_status else None,
            "booking_date": b.booking_date.isoformat() if b.booking_date else None,
        })
    return jsonify({"participants": participants})

@bp.route("/treks/<int:trek_id>/participants/<int:booking_id>/status", methods=["PUT"])
@token_auth_required
@roles_required(RoleEnum.STAFF)
def update_participant_status(trek_id, booking_id):
    staff = g.current_user
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    if trek.assigned_staff_id != staff.id:
        return jsonify({"error": "Not authorized for this trek"}), 403
    booking = Booking.query.get(booking_id)
    if not booking or booking.trek_id != trek.id:
        return jsonify({"error": "Booking not found for this trek"}), 404
    payload = get_request_data()
    
    from validations.user_validators import validate_booking_status_update
    is_valid, error = validate_booking_status_update(payload)
    if not is_valid:
        return jsonify({"error": error}), 400

    status = payload.get("status")
    booking.status = BookingStatusEnum(status)
    db.session.commit()
    return jsonify({"message": "Booking status updated", "booking": {"id": booking.id, "status": booking.status.value}})

@bp.route("/treks/<int:trek_id>/start", methods=["PUT"])
@token_auth_required
@roles_required(RoleEnum.STAFF)
def start_trek(trek_id):
    staff = g.current_user
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    if trek.assigned_staff_id != staff.id:
        return jsonify({"error": "Not authorized for this trek"}), 403
    trek.status = TrekStatusEnum.OPEN
    db.session.commit()
    return jsonify({"message": "Trek started", "trek": {"id": trek.id, "status": trek.status.value}})

@bp.route("/treks/<int:trek_id>/complete", methods=["PUT"])
@token_auth_required
@roles_required(RoleEnum.STAFF)
def complete_trek(trek_id):
    staff = g.current_user
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    if trek.assigned_staff_id != staff.id:
        return jsonify({"error": "Not authorized for this trek"}), 403
    trek.status = TrekStatusEnum.COMPLETED
    db.session.commit()
    return jsonify({"message": "Trek completed", "trek": {"id": trek.id, "status": trek.status.value}})
