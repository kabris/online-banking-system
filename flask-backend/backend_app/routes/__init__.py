from flask import Blueprint, jsonify

# Create a Blueprint for general routes
main_routes = Blueprint("main_routes", __name__)

@main_routes.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running!"})
