from backend import db

class UserNotification(db.Model):
    __tablename__ = 'user_notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="unread")  # unread, read
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_notifications(user_id):
        return UserNotification.query.filter_by(user_id=user_id).all()

    @staticmethod
    def mark_as_read(notification_id):
        notification = UserNotification.query.get(notification_id)
        if notification:
            notification.status = "read"
            db.session.commit()
