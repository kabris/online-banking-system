from flask import Blueprint, request, jsonify
import mysql.connector
import jwt
import datetime
from backend_app.models import db

auth_bp = Blueprint("auth", __name__)  # ✅ Create Authentication Blueprint

# ✅ Secret key for JWT authentication
SECRET_KEY = "your_secret_key"

@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")  # Can be email or account number
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    # ✅ Connect to MySQL
    try:
        cursor = db.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s OR account_number = %s", (username, username))
        user = cursor.fetchone()
        cursor.close()
    except Exception as e:
        return jsonify({"message": f"Database error: {str(e)}"}), 500

    if user:
        if user["password"] == password:  # Ensure to hash passwords in production!
            # ✅ Generate JWT Token
            token = jwt.encode({
                "user_id": user["id"],
                "role": user["role"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            }, SECRET_KEY, algorithm="HS256")

            return jsonify({"token": token, "role": user["role"]}), 200
        else:
            return jsonify({"message": "Invalid login credentials"}), 401
    else:
        return jsonify({"message": "User not found"}), 404
