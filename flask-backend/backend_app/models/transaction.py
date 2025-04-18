from backend_app.models import db

class Transaction(db.Model):
    __tablename__ = "transactions"  # ✅ Ensure this matches the DB table name
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(8), db.ForeignKey('user.account_number'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Transaction {self.id} - {self.amount}>"
