from backend_app.models import db

class SecurityAlert(db.Model):
    __tablename__ = "security_alerts"  # ✅ Ensure this matches the DB table name
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<SecurityAlert {self.alert_type}>"
