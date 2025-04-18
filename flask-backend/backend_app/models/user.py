from backend_app.models import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    account_number = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # ✅ Hash password before saving
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # ✅ Verify hashed password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
