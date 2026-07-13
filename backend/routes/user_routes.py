from flask import Blueprint, g, jsonify, request

from models import db
from models.models import Booking, BookingStatusEnum, PaymentStatusEnum, RoleEnum, Trek, TrekStatusEnum
from routes.auth_routes import token_auth_required, user_to_dict, get_request_data
from extensions import cache

bp = Blueprint("user", __name__)


@bp.route("/dashboard", methods=["GET"])
@token_auth_required
def dashboard():
    # fetch the logged in user
    user = g.current_user
    
    # only show treks that are approved or currently open
    available = Trek.query.filter(Trek.status.in_([TrekStatusEnum.APPROVED, TrekStatusEnum.OPEN])).order_by(Trek.id.desc()).all()
    available_list = []
    for t in available:
        available_list.append({
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "status": t.status.value if t.status else None,
            "available_slots": t.available_slots,
            "slots_remaining": t.slots_remaining(),
            "start_date": t.start_date.isoformat() if t.start_date else None,
            "end_date": t.end_date.isoformat() if t.end_date else None,
        })

    bookings = []
    for b in user.bookings:
        bookings.append({
            "id": b.id,
            "trek": {"id": b.trek.id, "name": b.trek.name, "location": b.trek.location, "end_date": b.trek.end_date.isoformat() if b.trek.end_date else None} if b.trek else None,
            "status": b.status.value if b.status else None,
            "payment_status": b.payment_status.value if b.payment_status else None,
            "booking_date": b.booking_date.isoformat() if b.booking_date else None,
        })

    return jsonify({"available_treks": available_list, "booked_treks": bookings})


@bp.route("/treks", methods=["GET"])
@cache.cached(timeout=300)
def list_treks():
    treks = Trek.query.filter(
        Trek.status.in_([TrekStatusEnum.APPROVED, TrekStatusEnum.OPEN])
    ).order_by(Trek.id.desc()).all()
    out = []
    for t in treks:
        out.append({
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "difficulty": t.difficulty.value if t.difficulty else None,
            "duration_days": t.duration_days,
            "status": t.status.value if t.status else None,
            "available_slots": t.available_slots,
            "slots_remaining": t.slots_remaining(),
            "start_date": t.start_date.isoformat() if t.start_date else None,
            "end_date": t.end_date.isoformat() if t.end_date else None,
        })
    return jsonify({"treks": out})


@bp.route("/treks/<int:trek_id>/book", methods=["POST"])
@token_auth_required
def book_trek(trek_id):
    user = g.current_user
    
    # block inactive accounts
    if not user.is_active:
        return jsonify({"error": "Your account is deactivated"}), 403
        
    trek = db.session.get(Trek, trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    if trek.status != TrekStatusEnum.OPEN:
        return jsonify({"error": "Booking is only allowed for Open treks"}), 400
    if trek.slots_remaining() <= 0:
        return jsonify({"error": "No slots available"}), 400
    # allow user to rebook if they previously cancelled
    existing = Booking.query.filter_by(user_id=user.id, trek_id=trek.id).first()
    if existing and existing.status != BookingStatusEnum.CANCELLED:
        return jsonify({"error": "You have already booked this trek"}), 400
        
    # revive the cancelled booking instead of creating a duplicate
    if existing and existing.status == BookingStatusEnum.CANCELLED:
        existing.status = BookingStatusEnum.BOOKED
        existing.payment_status = PaymentStatusEnum.PENDING
        db.session.commit()
        try:
            from tasks.notifications import send_booking_confirmation
            send_booking_confirmation.delay(existing.id)
        except Exception:
            pass
        return jsonify({"message": "Trek re-booked successfully", "booking": {"id": existing.id, "trek_id": trek.id, "status": existing.status.value}}), 201
    payload = get_request_data()
    booking = Booking(user_id=user.id, trek_id=trek.id)
    if "extra" in payload:
        booking.extra = payload.get("extra")
    booking.payment_status = PaymentStatusEnum.PENDING
    db.session.add(booking)
    db.session.commit()
    try:
        from tasks.notifications import send_booking_confirmation
        send_booking_confirmation.delay(booking.id)
    except Exception:
        pass
    return jsonify({"message": "Trek booked successfully", "booking": {"id": booking.id, "trek_id": trek.id, "status": booking.status.value}}), 201


@bp.route("/bookings", methods=["GET"])
@token_auth_required
def list_bookings():
    user = g.current_user
    out = []
    for b in user.bookings:
        out.append({
            "id": b.id,
            "trek": {"id": b.trek.id, "name": b.trek.name, "location": b.trek.location, "end_date": b.trek.end_date.isoformat() if b.trek.end_date else None} if b.trek else None,
            "status": b.status.value if b.status else None,
            "payment_status": b.payment_status.value if b.payment_status else None,
            "booking_date": b.booking_date.isoformat() if b.booking_date else None,
        })
    return jsonify({"bookings": out})


@bp.route("/bookings/<int:booking_id>", methods=["GET"])
@token_auth_required
def get_booking(booking_id):
    user = g.current_user
    booking = db.session.get(Booking, booking_id)
    if not booking or booking.user_id != user.id:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify({
        "booking": {
            "id": booking.id,
            "trek": {"id": booking.trek.id, "name": booking.trek.name, "location": booking.trek.location, "end_date": booking.trek.end_date.isoformat() if booking.trek.end_date else None} if booking.trek else None,
            "status": booking.status.value if booking.status else None,
            "payment_status": booking.payment_status.value if booking.payment_status else None,
            "booking_date": booking.booking_date.isoformat() if booking.booking_date else None,
            "extra": booking.extra,
        }
    })


@bp.route("/history", methods=["GET"])
@token_auth_required
def history():
    user = g.current_user
    # filter for past trips only (completed or cancelled)
    past = [b for b in user.bookings if b.status == BookingStatusEnum.COMPLETED or b.status == BookingStatusEnum.CANCELLED]
    out = []
    for b in past:
        out.append({
            "id": b.id,
            "trek": {"id": b.trek.id, "name": b.trek.name, "location": b.trek.location, "end_date": b.trek.end_date.isoformat() if b.trek.end_date else None} if b.trek else None,
            "status": b.status.value if b.status else None,
            "payment_status": b.payment_status.value if b.payment_status else None,
            "booking_date": b.booking_date.isoformat() if b.booking_date else None,
        })
    return jsonify({"history": out})


@bp.route("/profile", methods=["PUT"])
@token_auth_required
def edit_profile():
    user = g.current_user
    payload = get_request_data()
    
    from validations.user_validators import validate_profile_update
    is_valid, error = validate_profile_update(payload)
    if not is_valid:
        return jsonify({"error": error}), 400
        
    if "name" in payload:
        user.name = payload.get("name")
    if "phone" in payload:
        user.phone = payload.get("phone")
    if "password" in payload and payload.get("password"):
        user.set_password(payload.get("password"))
    db.session.commit()
    return jsonify({"message": "Profile updated", "user": user_to_dict(user)})


@bp.route("/treks/search", methods=["GET"])
@cache.cached(timeout=300, query_string=True)
def search_treks():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"treks": []})
    qlike = f"%{q}%"
    treks = Trek.query.filter((Trek.name.ilike(qlike)) | (Trek.location.ilike(qlike))).order_by(Trek.id.desc()).all()
    out = []
    for t in treks:
        out.append({
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "status": t.status.value if t.status else None,
            "slots_remaining": t.slots_remaining(),
        })
    return jsonify({"treks": out})


@bp.route("/export", methods=["POST"])
@token_auth_required
def export_history():
    user = g.current_user
    from tasks.exports import export_history_task
    export_history_task.delay(user.id)
    return jsonify({"message": "Export started. You will receive an email shortly with the CSV file attached."})

