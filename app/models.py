# app/models.py
from app import db


class IncomeExpense(db.Model):
    __tablename__ = 'income_expense'
    id = db.Column(db.Integer, primary_key=True)
    # Changed name to type, and removed unique=True
    type = db.Column(db.String(20), nullable=False)
    transactions = db.relationship(
        'Transaction', back_populates='income_expense')


class Shop(db.Model):
    __tablename__ = 'shop'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    transactions = db.relationship('Transaction', back_populates='shop')


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    subcategories = db.relationship('Subcategory', back_populates='category')
    # New relationship for direct access from Category to its transactions
    transactions_via_category = db.relationship(
        'Transaction', back_populates='category')


class Subcategory(db.Model):
    __tablename__ = 'subcategory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)

    category = db.relationship('Category', back_populates='subcategories')
    transactions = db.relationship('Transaction', back_populates='subcategory')

    __table_args__ = (
        db.UniqueConstraint('name', 'category_id',
                            name='uix_subcategory_name_category'),
    )


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    income_expense_id = db.Column(db.Integer, db.ForeignKey(
        'income_expense.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    # Changed to Numeric for precision with monetary values
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    # Changed to Numeric for precision with monetary values
    price = db.Column(db.Numeric(10, 2), nullable=False)
    # Changed to Numeric for precision with monetary values
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    # shop_id can be null if a transaction doesn't have a specific shop (e.g., income)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=True)
    # Added category_id back for direct filtering
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey(
        'subcategory.id'), nullable=False)

    income_expense = db.relationship(
        'IncomeExpense', back_populates='transactions')
    shop = db.relationship('Shop', back_populates='transactions')
    # New relationship for direct access to Category
    category = db.relationship(
        'Category', back_populates='transactions_via_category')
    subcategory = db.relationship('Subcategory', back_populates='transactions')

    def __repr__(self):
        return f"<Transaction {self.name} on {self.date} ({self.amount})>"
