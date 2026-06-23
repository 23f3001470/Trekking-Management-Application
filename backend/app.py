import os

from flask import Flask
from celery.schedules import crontab
from celery_app import celery_init_app
from flask_mail import Mail
from models import db
from models.models import RoleEnum, User
from seeders.seed_users import seed_users
from routes.auth_routes import bp as auth_bp
from routes.admin_routes import bp as admin_bp
from routes.staff_routes import bp as staff_bp
from routes.user_routes import bp as user_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "trek-app-secret-key")

# Celery Configuration
app.config.from_mapping(
    CELERY=dict(
        broker_url="amqp://guest:guest@localhost:5672//",
        result_backend="rpc://",
        task_ignore_result=True,
        beat_schedule={
            "daily_reminders": {
                "task": "tasks.reminders.send_daily_reminders",
                "schedule": crontab(hour=8, minute=0), # Change hour/minute to test
            }
        }
    )
)

# Mail Configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'localhost')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 1025)) # Default to Mailhog or local test server
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'False').lower() in ['true', '1', 't']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@trekapp.com')

mail = Mail(app)
celery = celery_init_app(app)

# Import tasks after celery is initialized to register them
import tasks.reminders
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(staff_bp, url_prefix="/staff")
app.register_blueprint(user_bp, url_prefix="/user")

db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(role=RoleEnum.ADMIN).first():
        seed_users()
        print("Default admin and staff seeded.")
    else:
        print("Default admin and staff already present.")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
