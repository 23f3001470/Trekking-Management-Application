import csv
import io
from celery import shared_task
from flask_mail import Message
from models.models import Booking, User, BookingStatusEnum

@shared_task(name="tasks.exports.export_history_task")
def export_history_task(user_id):
    from app import mail
    
    user = User.query.get(user_id)
    if not user:
        return "User not found"
        
    bookings = Booking.query.filter_by(user_id=user.id).all()
    
    # filter past bookings
    past_bookings = [b for b in bookings if b.status in [BookingStatusEnum.COMPLETED, BookingStatusEnum.CANCELLED]]
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["User ID", "Trek Name", "Location", "Booking Status", "Start Date", "End Date"])
    
    for b in past_bookings:
        trek_name = b.trek.name if b.trek else "Unknown"
        location = b.trek.location if b.trek else "Unknown"
        status = b.status.value if b.status else "Unknown"
        start_date = b.trek.start_date.isoformat() if (b.trek and b.trek.start_date) else ""
        end_date = b.trek.end_date.isoformat() if (b.trek and b.trek.end_date) else ""
        writer.writerow([user.id, trek_name, location, status, start_date, end_date])
        
    csv_data = output.getvalue()
    
    msg = Message(
        subject="Your Trekking History Export",
        recipients=[user.email],
        body=f"Hello {user.name},\n\nPlease find attached your trekking history CSV file.\n\nBest regards,\nTrekking Management Team"
    )
    
    msg.attach("trekking_history.csv", "text/csv", csv_data)
    
    try:
        mail.send(msg)
        return f"Export sent to {user.email}"
    except Exception as e:
        return f"Failed to send export: {e}"
