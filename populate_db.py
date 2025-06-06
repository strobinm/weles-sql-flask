import json
from datetime import datetime
from app import create_app, db  # Adjust import based on your project structure
# Import your models
from app.models import IncomeExpense, Shop, Category, Subcategory, Transaction


def populate_database(json_file_path):
    app = create_app()
    with app.app_context():
        print("Starting database population...")

        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Ensure "Przychody" and "Wydatki" exist in IncomeExpense table
        income_type = IncomeExpense.query.filter_by(type="Przychody").first()
        if not income_type:
            income_type = IncomeExpense(type="Przychody")
            db.session.add(income_type)
        expense_type = IncomeExpense.query.filter_by(type="Wydatki").first()
        if not expense_type:
            expense_type = IncomeExpense(type="Wydatki")
            db.session.add(expense_type)
        db.session.commit()  # Commit these initial types

        # Iterate through your JSON data
        for entry in data:
            # 1. Handle IncomeExpense relationship
            income_expense_obj = IncomeExpense.query.filter_by(
                type=entry['Przychody/Wydatki']).first()
            if not income_expense_obj:
                # This should ideally not happen if you pre-populated "Przychody" and "Wydatki"
                print(
                    f"Warning: IncomeExpense type '{entry['Przychody/Wydatki']}' not found. Adding it.")
                income_expense_obj = IncomeExpense(
                    type=entry['Przychody/Wydatki'])
                db.session.add(income_expense_obj)
                db.session.commit()

            # 2. Handle Shop (can be nullable)
            shop_obj = None
            if entry['Sklep']:  # Check if shop name exists in JSON
                shop_obj = Shop.query.filter_by(name=entry['Sklep']).first()
                if not shop_obj:
                    shop_obj = Shop(name=entry['Sklep'])
                    db.session.add(shop_obj)
                    db.session.commit()  # Commit to get the shop_id

            # 3. Handle Category
            category_obj = Category.query.filter_by(
                name=entry['Kategoria']).first()
            if not category_obj:
                category_obj = Category(name=entry['Kategoria'])
                db.session.add(category_obj)
                db.session.commit()  # Commit to get the category_id

            # 4. Handle Subcategory (unique constraint on name and category_id)
            subcategory_obj = Subcategory.query.filter_by(
                name=entry['Podkategoria'],
                category_id=category_obj.id
            ).first()
            if not subcategory_obj:
                subcategory_obj = Subcategory(
                    name=entry['Podkategoria'],
                    category=category_obj  # Assign object, SQLAlchemy handles FK
                )
                db.session.add(subcategory_obj)
                db.session.commit()  # Commit to get the subcategory_id

            # 5. Create Transaction
            new_transaction = Transaction(
                date=datetime.strptime(entry['Data'], '%Y-%m-%d').date(),
                income_expense=income_expense_obj,  # Assign object
                name=entry['Nazwa'],
                # Ensure correct type conversion
                quantity=float(entry['Ilość']),
                # Ensure correct type conversion
                price=float(entry['Cena']),
                # Ensure correct type conversion
                amount=float(entry['Kwota']),
                shop=shop_obj,  # Assign object (can be None)
                subcategory=subcategory_obj  # Assign object
            )
            db.session.add(new_transaction)

        db.session.commit()  # Commit all new transactions at once after the loop
        print("Database population complete!")


if __name__ == '__main__':
    # Replace 'your_data.json' with the actual path to your JSON file
    populate_database('data.json')
