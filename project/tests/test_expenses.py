from app import create_app, db
from app.models import Category, PaymentMethod


def make_app():
    return create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        }
    )


def test_index_loads_seeded_expenses():
    app = make_app()

    with app.test_client() as client:
        response = client.get("/")

    assert response.status_code == 200
    assert b"Zakupy spozywcze" in response.data


def test_create_expense_requires_positive_amount():
    app = make_app()

    with app.app_context():
        category = Category.query.first()
        method = PaymentMethod.query.first()

    with app.test_client() as client:
        response = client.post(
            "/expenses/new",
            data={
                "title": "Test",
                "amount": "-1",
                "spent_on": "2026-06-07",
                "category_id": str(category.id),
                "payment_method_id": str(method.id),
            },
        )

    assert response.status_code == 200
    assert "Kwota musi byc wieksza od zera.".encode() in response.data


def test_search_filters_expenses():
    app = make_app()

    with app.test_client() as client:
        response = client.get("/?search=Kino")

    assert response.status_code == 200
    assert b"Kino" in response.data
    assert b"Bilet miesieczny" not in response.data
