from datetime import date

from app import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    color = db.Column(db.String(20), nullable=False, default="#2563eb")
    expenses = db.relationship("Expense", back_populates="category", lazy=True)


class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    expenses = db.relationship("Expense", back_populates="payment_method", lazy=True)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    spent_on = db.Column(db.Date, nullable=False, default=date.today)
    note = db.Column(db.String(250), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    payment_method_id = db.Column(
        db.Integer, db.ForeignKey("payment_method.id"), nullable=False
    )

    category = db.relationship("Category", back_populates="expenses")
    payment_method = db.relationship("PaymentMethod", back_populates="expenses")


def seed_database():
    if Category.query.first():
        return

    categories = [
        Category(name="Jedzenie", color="#16a34a"),
        Category(name="Transport", color="#2563eb"),
        Category(name="Dom", color="#ea580c"),
        Category(name="Rozrywka", color="#9333ea"),
    ]
    payment_methods = [
        PaymentMethod(name="Karta"),
        PaymentMethod(name="Gotowka"),
        PaymentMethod(name="Przelew"),
    ]

    db.session.add_all(categories + payment_methods)
    db.session.commit()

    demo_expenses = [
        Expense(
            title="Zakupy spozywcze",
            amount=84.50,
            spent_on=date(2026, 6, 1),
            category_id=categories[0].id,
            payment_method_id=payment_methods[0].id,
            note="Tygodniowe zakupy",
        ),
        Expense(
            title="Bilet miesieczny",
            amount=110.00,
            spent_on=date(2026, 6, 2),
            category_id=categories[1].id,
            payment_method_id=payment_methods[2].id,
        ),
        Expense(
            title="Kino",
            amount=38.00,
            spent_on=date(2026, 6, 3),
            category_id=categories[3].id,
            payment_method_id=payment_methods[0].id,
        ),
    ]

    db.session.add_all(demo_expenses)
    db.session.commit()
