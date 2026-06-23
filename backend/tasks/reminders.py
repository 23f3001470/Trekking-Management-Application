from celery import shared_task
from flask_mail import Message
from models.models import Trek, Booking, BookingStatusEnum, TrekStatusEnum
from datetime import date, timedelta

@shared_task(name="tasks.reminders.send_daily_reminders")
def send_daily_reminders():
    # Because of our custom FlaskTask, this will run inside app context automatically
    from app import mail
    
    tomorrow = date.today() + timedelta(days=1)
    
    upcoming_treks = Trek.query.filter(
        Trek.start_date == tomorrow,
        Trek.status.in_([TrekStatusEnum.APPROVED, TrekStatusEnum.OPEN, TrekStatusEnum.CLOSED])
    ).all()
    
    count = 0
    for trek in upcoming_treks:
        bookings = Booking.query.filter_by(trek_id=trek.id, status=BookingStatusEnum.BOOKED).all()
        
        for booking in bookings:
            user = booking.user
            
            msg = Message(
                subject=f"Reminder: Upcoming Trek to {trek.location} Tomorrow!",
                recipients=[user.email]
            )
            msg.body = f"Hello {user.name},\n\nThis is a reminder that your trek '{trek.name}' to {trek.location} is starting tomorrow ({tomorrow}).\n\nPlease ensure you follow all instructions and arrive on time.\n\nBest regards,\nTrekking Management Team"
            
            try:
                mail.send(msg)
                print(f"Sent reminder email to {user.email} for trek {trek.name}")
                count += 1
            except Exception as e:
                print(f"Failed to send email to {user.email}: {e}")
                
    return f"Sent {count} reminders."
