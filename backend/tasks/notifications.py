from celery import shared_task
from flask_mail import Message
from models.models import Booking, User, Trek
from models import db

@shared_task(name="tasks.notifications.send_booking_confirmation")
def send_booking_confirmation(booking_id):
    from app import mail
    
    booking = db.session.get(Booking, booking_id)
    if not booking:
        return f"Booking {booking_id} not found."
        
    user = booking.user
    trek = booking.trek
    
    if not user or not trek:
        return f"Missing user or trek for booking {booking_id}."
        
    msg = Message(
        subject=f"Booking Confirmation: {trek.name}",
        recipients=[user.email]
    )
    formatted_date = trek.start_date.strftime('%d-%m-%Y') if trek.start_date else 'TBD'
    
    msg.body = f"""Hello {user.name},

Your booking for the trek '{trek.name}' to {trek.location} has been confirmed!
Status: {booking.status.value}

Trek Details:
- Location: {trek.location}
- Start Date: {formatted_date}
- Difficulty: {trek.difficulty.value if hasattr(trek, 'difficulty') and trek.difficulty else 'Moderate'}

We look forward to seeing you. 
If you have any questions, please contact the support team.

Best regards,
Trekking Management Team
"""
    
    try:
        mail.send(msg)
        return f"Confirmation email sent to {user.email} for booking {booking_id}."
    except Exception as e:
        return f"Failed to send confirmation email to {user.email}: {e}"

@shared_task(name="tasks.notifications.send_booking_cancellation")
def send_booking_cancellation(booking_id):
    from app import mail
    
    booking = db.session.get(Booking, booking_id)
    if not booking:
        return f"Booking {booking_id} not found."
        
    user = booking.user
    trek = booking.trek
    
    if not user or not trek:
        return f"Missing user or trek for booking {booking_id}."
        
    msg = Message(
        subject=f"Booking Cancelled: {trek.name}",
        recipients=[user.email]
    )
    
    msg.body = f"""Hello {user.name},

We regret to inform you that your booking for the trek '{trek.name}' has been cancelled.

If you have already made a payment, it will be refunded according to our policy.
Please contact the support team for more details or to book another trek.

Best regards,
Trekking Management Team
"""
    
    try:
        mail.send(msg)
        return f"Cancellation email sent to {user.email} for booking {booking_id}."
    except Exception as e:
        return f"Failed to send cancellation email to {user.email}: {e}"
