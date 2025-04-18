from flask import Blueprint, request, jsonify
from backend_app.models import db, SecurityAlert

security_routes = Blueprint("security_routes", __name__)

@security_routes.route("/alerts", methods=["GET"])
def get_alerts():
    alerts = SecurityAlert.query.all()
    return jsonify([{"account_number": a.account_number, "alert_message": a.alert_message, "severity": a.severity} for a in alerts])
