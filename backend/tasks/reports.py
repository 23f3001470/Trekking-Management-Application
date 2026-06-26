from celery import shared_task
from flask_mail import Message
from models.models import Trek, Booking, BookingStatusEnum, TrekStatusEnum, User, RoleEnum, db
from datetime import date, timedelta
from sqlalchemy import func

@shared_task(name="tasks.reports.send_monthly_activity_report")
def send_monthly_activity_report():
    from app import mail
    
    today = date.today()
    last_day_of_last_month = today.replace(day=1) - timedelta(days=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)
    
    conducted_treks = Trek.query.filter(
        Trek.start_date >= first_day_of_last_month,
        Trek.start_date <= last_day_of_last_month,
        Trek.status == TrekStatusEnum.COMPLETED
    ).all()
    
    num_treks_conducted = len(conducted_treks)
    
    trek_ids = [t.id for t in conducted_treks]
    if trek_ids:
        num_users_participated = db.session.query(func.count(func.distinct(Booking.user_id))).filter(
            Booking.trek_id.in_(trek_ids),
            Booking.status.in_([BookingStatusEnum.BOOKED, BookingStatusEnum.COMPLETED])
        ).scalar()
    else:
        num_users_participated = 0

    treks_last_month = Trek.query.filter(
        Trek.start_date >= first_day_of_last_month,
        Trek.start_date <= last_day_of_last_month
    ).all()
    
    trek_booking_counts = []
    for t in treks_last_month:
        valid_bookings = [b for b in t.bookings if b.status in [BookingStatusEnum.BOOKED, BookingStatusEnum.COMPLETED]]
        trek_booking_counts.append((t, len(valid_bookings)))
        
    trek_booking_counts.sort(key=lambda x: x[1], reverse=True)
    top_treks = trek_booking_counts[:3]

    popular_treks_html = "<ul>\n"
    for t, count in top_treks:
        popular_treks_html += f"                <li><strong>{t.name}</strong> - {count} bookings</li>\n"
    popular_treks_html += "            </ul>"
    
    if not top_treks:
        popular_treks_html = "<p>No treks were booked last month.</p>"
        
    month_name = first_day_of_last_month.strftime("%B %Y")
        
    html_content = f"""
    <html>
        <body>
            <h2>Monthly Activity Report - {month_name}</h2>
            <p>Hello Admin,</p>
            <p>Here is the summary of trekking activities for the month of {month_name}:</p>
            <ul>
                <li><strong>Number of Treks Conducted:</strong> {num_treks_conducted}</li>
                <li><strong>Number of Unique Participants:</strong> {num_users_participated}</li>
            </ul>
            <h3>Popular Treks</h3>
            {popular_treks_html}
            <br>
            <p>Best regards,</p>
            <p>Trekking Management Team</p>
        </body>
    </html>
    """
    
    admins = User.query.filter_by(role=RoleEnum.ADMIN, is_active=True).all()
    admin_emails = [admin.email for admin in admins]
    
    if not admin_emails:
        return "No admins found to send report."
        
    msg = Message(
        subject=f"Monthly Activity Report - {month_name}",
        recipients=admin_emails,
        html=html_content
    )
    
    try:
        mail.send(msg)
        return f"Sent monthly report for {month_name} to {len(admin_emails)} admins."
    except Exception as e:
        return f"Failed to send monthly report: {e}"
