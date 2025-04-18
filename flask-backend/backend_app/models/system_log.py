from backend_app.models import db

class SystemLog(db.Model):
    __tablename__ = "system_logs"  # ✅ Ensure this matches the DB table name
    id = db.Column(db.Integer, primary_key=True)
    log_type = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<SystemLog {self.log_type}>"
