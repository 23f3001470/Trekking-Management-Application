import os

from flask import Flask

from models import db
from models.models import RoleEnum, User
from seeders.seed_users import seed_users
from routes.auth_routes import bp as auth_bp
from routes.admin_routes import bp as admin_bp
from routes.staff_routes import bp as staff_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "trek-app-secret-key")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(staff_bp, url_prefix="/staff")

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
