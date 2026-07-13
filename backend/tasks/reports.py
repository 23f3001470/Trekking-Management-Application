from celery import shared_task
from flask_mail import Message
from models.models import Trek, Booking, BookingStatusEnum, TrekStatusEnum, User, RoleEnum, db
from datetime import date, timedelta
from sqlalchemy import func
import io
from xhtml2pdf import pisa

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

    popular_treks_html = ""
    for t, count in top_treks:
        popular_treks_html += f"<tr><td>{t.name}</td><td>{t.location}</td><td style='text-align: right;'>{count}</td></tr>\n"
    
    if not top_treks:
        popular_treks_html = "<tr><td colspan='3' style='text-align: center;'>No treks were booked last month.</td></tr>"
        
    month_name = first_day_of_last_month.strftime("%B %Y")
        
    pdf_html_content = f"""
    <html>
        <head>
            <style>
                @page {{
                    size: a4 portrait;
                    margin: 2cm;
                }}
                body {{
                    font-family: Helvetica, Arial, sans-serif;
                    color: #333;
                }}
                .header {{
                    text-align: center;
                    border-bottom: 2px solid #2ecc71;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    color: #2c3e50;
                    margin: 0;
                    font-size: 28px;
                }}
                .header p {{
                    color: #7f8c8d;
                    margin: 5px 0 0 0;
                    font-size: 16px;
                }}
                .summary-box {{
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 8px;
                    padding: 20px;
                    margin-bottom: 30px;
                }}
                .summary-box h3 {{
                    margin-top: 0;
                    color: #2c3e50;
                    border-bottom: 1px solid #dee2e6;
                    padding-bottom: 10px;
                }}
                .stat-grid {{
                    width: 100%;
                }}
                .stat-grid td {{
                    width: 50%;
                    padding: 10px 0;
                }}
                .stat-label {{
                    font-weight: bold;
                    color: #7f8c8d;
                    font-size: 14px;
                }}
                .stat-value {{
                    font-size: 24px;
                    color: #2c3e50;
                    font-weight: bold;
                }}
                table.data-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                table.data-table th, table.data-table td {{
                    border: 1px solid #dee2e6;
                    padding: 12px;
                    text-align: left;
                }}
                table.data-table th {{
                    background-color: #f8f9fa;
                    color: #495057;
                    font-weight: bold;
                }}
                .footer {{
                    margin-top: 50px;
                    text-align: center;
                    color: #adb5bd;
                    font-size: 12px;
                    border-top: 1px solid #dee2e6;
                    padding-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Trekking Management Application</h1>
                <p>Monthly Activity Report - {month_name}</p>
            </div>
            
            <div class="summary-box">
                <h3>Executive Summary</h3>
                <table class="stat-grid">
                    <tr>
                        <td>
                            <div class="stat-label">Total Treks Conducted</div>
                            <div class="stat-value">{num_treks_conducted}</div>
                        </td>
                        <td>
                            <div class="stat-label">Unique Participants</div>
                            <div class="stat-value">{num_users_participated}</div>
                        </td>
                    </tr>
                </table>
            </div>

            <h3 style="color: #2c3e50; margin-bottom: 15px;">Popular Treks</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Trek Name</th>
                        <th>Location</th>
                        <th style="text-align: right;">Bookings</th>
                    </tr>
                </thead>
                <tbody>
                    {popular_treks_html}
                </tbody>
            </table>
            
            <div class="footer">
                <p>Generated automatically by the Trekking Management Application.</p>
                <p>&copy; {date.today().year} All rights reserved.</p>
            </div>
        </body>
    </html>
    """
    
    email_html_content = f"""
    <html>
        <body>
            <h2>Monthly Activity Report - {month_name}</h2>
            <p>Hello Admin,</p>
            <p>The activity report for {month_name} is ready. We have generated a detailed PDF report for your review.</p>
            <p><strong>Quick Summary:</strong></p>
            <ul>
                <li>Treks Conducted: {num_treks_conducted}</li>
                <li>Unique Participants: {num_users_participated}</li>
            </ul>
            <p>Please find the well-designed PDF report attached to this email.</p>
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
        
    # generate pdf
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(pdf_html_content), dest=pdf_buffer)
    
    if pisa_status.err:
        return "Failed to generate PDF report."
        
    msg = Message(
        subject=f"Monthly Activity Report - {month_name}",
        recipients=admin_emails,
        html=email_html_content
    )
    
    msg.attach(
        f"Monthly_Report_{month_name.replace(' ', '_')}.pdf",
        "application/pdf",
        pdf_buffer.getvalue()
    )
    
    try:
        mail.send(msg)
        return f"Sent monthly PDF report for {month_name} to {len(admin_emails)} admins."
    except Exception as e:
        return f"Failed to send monthly report: {e}"
