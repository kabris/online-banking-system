from flask import Blueprint, request, jsonify
from backend_app.models import db, Transaction

transaction_routes = Blueprint("transaction_routes", __name__)

@transaction_routes.route("/transactions", methods=["GET"])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([{"account_number": t.account_number, "amount": t.amount, "status": t.status} for t in transactions])
