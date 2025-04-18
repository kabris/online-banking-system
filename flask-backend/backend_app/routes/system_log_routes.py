from flask import Blueprint, request, jsonify
from backend_app.models import db, SystemLog

system_log_routes = Blueprint("system_log_routes", __name__)

@system_log_routes.route("/logs", methods=["GET"])
def get_logs():
    logs = SystemLog.query.all()
    return jsonify([{"action": l.action, "performed_by": l.performed_by} for l in logs])
