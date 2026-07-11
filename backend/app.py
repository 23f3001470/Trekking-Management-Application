import os
from dotenv import load_dotenv

load_dotenv()
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
from extensions import cache

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "trek-app-secret-key")
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

app.config.from_mapping(
    CELERY=dict(
        broker_url="amqp://guest:guest@localhost:5672//",
        result_backend="rpc://",
        task_ignore_result=True,
        beat_schedule={
            "daily_reminders": {
                "task": "tasks.reminders.send_daily_reminders",
                "schedule": crontab(hour=8, minute=0),
            },
            "monthly_report": {
                "task": "tasks.reports.send_monthly_activity_report",
                "schedule": crontab(day_of_month="1", hour=8, minute=0),
            }
        }
    )
)

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'localhost')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 1025))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'False').lower() in ['true', '1', 't']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@trekapp.com')

cache.init_app(app)
mail = Mail(app)
celery = celery_init_app(app)

import tasks.reminders
import tasks.reports
import tasks.exports
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
