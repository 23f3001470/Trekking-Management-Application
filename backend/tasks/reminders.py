from celery import shared_task
from flask_mail import Message
from models.models import Trek, Booking, BookingStatusEnum, TrekStatusEnum, User, RoleEnum
from datetime import date, timedelta

@shared_task(name="tasks.reminders.send_daily_reminders")
def send_daily_reminders():
    from app import mail
    
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    users = User.query.filter_by(role=RoleEnum.USER, is_active=True).all()
    
    count_reminders = 0
    count_greetings = 0
    
    for user in users:
        user_bookings = Booking.query.filter_by(user_id=user.id, status=BookingStatusEnum.BOOKED).all()
        has_upcoming_trek = False
        
        for booking in user_bookings:
            trek = booking.trek
            if trek.start_date in [today, tomorrow] and trek.status in [TrekStatusEnum.PENDING, TrekStatusEnum.APPROVED, TrekStatusEnum.OPEN, TrekStatusEnum.CLOSED]:
                when = "Today" if trek.start_date == today else "Tomorrow"
                msg = Message(
                    subject=f"Reminder: Upcoming Trek to {trek.location} {when}!",
                    recipients=[user.email]
                )
                formatted_date = trek.start_date.strftime('%d-%m-%Y')
                msg.body = f"Hello {user.name},\n\nThis is a reminder that your trek '{trek.name}' to {trek.location} is starting {when.lower()} ({formatted_date}).\n\nPlease ensure you follow all instructions and arrive on time.\n\nBest regards,\nTrekking Management Team"
                
                try:
                    mail.send(msg)
                    print(f"Sent reminder email to {user.email} for trek {trek.name}")
                    count_reminders += 1
                except Exception as e:
                    print(f"Failed to send email to {user.email}: {e}")
                    
                has_upcoming_trek = True
                break
                
        if not has_upcoming_trek:
            msg = Message(
                subject="Ready for your next adventure?",
                recipients=[user.email]
            )
            msg.body = f"Hello {user.name},\n\nWe noticed you don't have any treks starting today or tomorrow. Why not plan your next adventure?\nCheck out our available upcoming treks and book your slot today!\n\nBest regards,\nTrekking Management Team"
            
            try:
                mail.send(msg)
                print(f"Sent greeting email to {user.email}")
                count_greetings += 1
            except Exception as e:
                print(f"Failed to send greeting to {user.email}: {e}")
                
    return f"Sent {count_reminders} reminders and {count_greetings} greetings."
