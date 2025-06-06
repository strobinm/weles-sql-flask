# run.py
from app import create_app, db
# Import your models
from app.models import IncomeExpense, Shop, Category, Subcategory, Transaction

app = create_app()


@app.cli.command("create-tables")
def create_tables():
    """Create database tables."""
    with app.app_context():
        db.create_all()
        print("Tables created successfully.")


@app.cli.command("drop-tables")
def drop_tables():
    """Drop all database tables."""
    with app.app_context():
        db.drop_all()
        print("Tables dropped successfully.")


if __name__ == '__main__':
    app.run(debug=True)
