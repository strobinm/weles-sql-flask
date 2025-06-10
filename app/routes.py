from flask import Blueprint, jsonify
from app.models import Transaction

routes = Blueprint('routes', __name__)


@routes.route("/api/transactions")
def get_transactions():
    # Query all transactions, ordered by ID descending
    transactions = Transaction.query.order_by(Transaction.id.desc()).all()

    result = []
    for t in transactions:
        result.append({
            "date": t.date.isoformat(),
            "type": t.income_expense.type if t.income_expense else None,
            "name": t.name,
            "quantity": float(t.quantity),
            "price": float(t.price),
            "amount": float(t.amount),
            "shop": t.shop.name if t.shop else None,
            "category": t.category.name if t.category else None,
            "subcategory": t.subcategory.name if t.subcategory else None,
        })

    return jsonify(result)
