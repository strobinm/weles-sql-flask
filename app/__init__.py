from flask import Flask, render_template, request, url_for, redirect
from app.extensions import db
from app.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from app.routes import routes
# No longer need extract, distinct here as they are used in filters.py
# from sqlalchemy import extract, distinct



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)

    # Import models and filters after db is initialized to avoid circular imports
    from app.models import IncomeExpense, Shop, Category, Subcategory, Transaction
    # Register the blueprint
    app.register_blueprint(routes)

    @app.route('/')
    def home():
        # Pass data to the template
        return render_template(
            'index.html'
            )

    @app.route('/about')
    def about():
        return "This is the About page."

    @app.route('/add')
    def add():
        return "Here you will add expenses."

    return app
