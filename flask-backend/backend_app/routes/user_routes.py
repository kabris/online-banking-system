from flask import Blueprint, request, jsonify
from backend_app.models import db, User

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"account_number": u.account_number, "name": u.name, "email": u.email} for u in users])
