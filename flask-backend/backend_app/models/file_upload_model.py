from backend_app.models import db

class FileUpload(db.Model):
    __tablename__ = "file_uploads"  # ✅ Ensure this matches the DB table name

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<FileUpload {self.filename}>"
