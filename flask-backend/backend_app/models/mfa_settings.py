from backend import db

class MFASettings(db.Model):
    __tablename__ = 'mfa_settings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False, unique=True)
    mfa_enabled = db.Column(db.Boolean, default=False)
    mfa_type = db.Column(db.String(50), default="None")  # e.g., "SMS", "Email", "Authenticator App"
    secret_key = db.Column(db.String(255), nullable=True)  # For storing OTP secret keys
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, user_id, mfa_enabled, mfa_type, secret_key):
        self.user_id = user_id
        self.mfa_enabled = mfa_enabled
        self.mfa_type = mfa_type
        self.secret_key = secret_key

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_mfa_settings(user_id):
        return MFASettings.query.filter_by(user_id=user_id).first()

    @staticmethod
    def update_mfa(user_id, mfa_enabled, mfa_type, secret_key):
        mfa = MFASettings.query.filter_by(user_id=user_id).first()
        if mfa:
            mfa.mfa_enabled = mfa_enabled
            mfa.mfa_type = mfa_type
            mfa.secret_key = secret_key
            db.session.commit()
