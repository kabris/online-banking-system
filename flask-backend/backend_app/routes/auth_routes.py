from flask import Blueprint, request, jsonify
from backend_app.models.user import User
from backend_app import db
from backend_app.config import Config
import jwt
import datetime

auth_routes = Blueprint("auth_routes", __name__)

# ✅ User Registration
@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    role = data.get("role")

    if not email or not password or not name or not role:
        return jsonify({"error": "All fields are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    user = User(email=email, name=name, role=role)
    user.set_password(password)  # ✅ Hash password before saving

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# ✅ User Login
@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    # ✅ Generate JWT Token
    token = jwt.encode(
        {"user_id": user.account_number, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)},
        Config.JWT_SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"message": "Login successful", "token": token})
