from backend import db

class DeletedUser(db.Model):
    __tablename__ = 'delete_users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(50), nullable=False)
    deleted_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, user_id, full_name, email, role):
        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.role = role

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_deleted_users():
        return DeletedUser.query.all()
