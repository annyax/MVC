from datetime import datetime
from decimal import Decimal, InvalidOperation

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.models import Category, Expense, PaymentMethod


main_bp = Blueprint("main", __name__)


def expense_query():
    query = Expense.query.join(Category).join(PaymentMethod)
    search = request.args.get("search", "").strip()
    category_id = request.args.get("category_id", "").strip()
    payment_method_id = request.args.get("payment_method_id", "").strip()

    if search:
        query = query.filter(Expense.title.ilike(f"%{search}%"))
    if category_id:
        query = query.filter(Expense.category_id == int(category_id))
    if payment_method_id:
        query = query.filter(Expense.payment_method_id == int(payment_method_id))

    return query.order_by(Expense.spent_on.desc(), Expense.id.desc())


def validate_expense(form):
    errors = []
    title = form.get("title", "").strip()
    amount_raw = form.get("amount", "").strip()
    spent_on_raw = form.get("spent_on", "").strip()
    note = form.get("note", "").strip()
    category_id = form.get("category_id", "").strip()
    payment_method_id = form.get("payment_method_id", "").strip()

    if not title:
        errors.append("Nazwa wydatku jest wymagana.")
    elif len(title) > 100:
        errors.append("Nazwa wydatku moze miec maksymalnie 100 znakow.")

    try:
        amount = Decimal(amount_raw)
        if amount <= 0:
            errors.append("Kwota musi byc wieksza od zera.")
    except (InvalidOperation, ValueError):
        amount = None
        errors.append("Kwota musi byc poprawna liczba.")

    try:
        spent_on = datetime.strptime(spent_on_raw, "%Y-%m-%d").date()
    except ValueError:
        spent_on = None
        errors.append("Data musi byc w formacie RRRR-MM-DD.")

    category = db.session.get(Category, int(category_id)) if category_id.isdigit() else None
    payment_method = (
        db.session.get(PaymentMethod, int(payment_method_id))
        if payment_method_id.isdigit()
        else None
    )

    if not category:
        errors.append("Wybierz poprawna kategorie.")
    if not payment_method:
        errors.append("Wybierz poprawna metode platnosci.")
    if len(note) > 250:
        errors.append("Notatka moze miec maksymalnie 250 znakow.")

    data = {
        "title": title,
        "amount": amount,
        "spent_on": spent_on,
        "note": note,
        "category_id": category.id if category else None,
        "payment_method_id": payment_method.id if payment_method else None,
    }
    return errors, data


def form_context(expense=None, errors=None):
    return {
        "expense": expense,
        "errors": errors or [],
        "categories": Category.query.order_by(Category.name).all(),
        "payment_methods": PaymentMethod.query.order_by(PaymentMethod.name).all(),
    }


@main_bp.route("/")
def index():
    expenses = expense_query().all()
    total = sum(expense.amount for expense in expenses)
    return render_template(
        "expenses/index.html",
        expenses=expenses,
        categories=Category.query.order_by(Category.name).all(),
        payment_methods=PaymentMethod.query.order_by(PaymentMethod.name).all(),
        total=total,
        filters=request.args,
    )


@main_bp.route("/expenses/<int:expense_id>")
def details(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    return render_template("expenses/details.html", expense=expense)


@main_bp.route("/expenses/new", methods=["GET", "POST"])
def create_expense():
    if request.method == "POST":
        errors, data = validate_expense(request.form)
        if not errors:
            expense = Expense(**data)
            db.session.add(expense)
            db.session.commit()
            flash("Wydatek zostal dodany.", "success")
            return redirect(url_for("main.index"))
        return render_template("expenses/form.html", **form_context(errors=errors))

    return render_template("expenses/form.html", **form_context())


@main_bp.route("/expenses/<int:expense_id>/edit", methods=["GET", "POST"])
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if request.method == "POST":
        errors, data = validate_expense(request.form)
        if not errors:
            for field, value in data.items():
                setattr(expense, field, value)
            db.session.commit()
            flash("Wydatek zostal zaktualizowany.", "success")
            return redirect(url_for("main.details", expense_id=expense.id))
        return render_template(
            "expenses/form.html", **form_context(expense=expense, errors=errors)
        )

    return render_template("expenses/form.html", **form_context(expense=expense))


@main_bp.route("/expenses/<int:expense_id>/delete", methods=["POST"])
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    flash("Wydatek zostal usuniety.", "success")
    return redirect(url_for("main.index"))
