from datetime import date

from django.db import migrations


def seed_data(apps, schema_editor):
    Category = apps.get_model("expenses", "Category")
    PaymentMethod = apps.get_model("expenses", "PaymentMethod")
    Expense = apps.get_model("expenses", "Expense")

    categories = {
        "Jedzenie": Category.objects.create(name="Jedzenie", color="#16a34a"),
        "Transport": Category.objects.create(name="Transport", color="#2563eb"),
        "Dom": Category.objects.create(name="Dom", color="#ea580c"),
        "Rozrywka": Category.objects.create(name="Rozrywka", color="#9333ea"),
    }
    methods = {
        "Karta": PaymentMethod.objects.create(name="Karta"),
        "Gotowka": PaymentMethod.objects.create(name="Gotowka"),
        "Przelew": PaymentMethod.objects.create(name="Przelew"),
    }

    Expense.objects.bulk_create(
        [
            Expense(
                title="Zakupy spozywcze",
                amount="84.50",
                spent_on=date(2026, 6, 1),
                category=categories["Jedzenie"],
                payment_method=methods["Karta"],
                note="Tygodniowe zakupy",
            ),
            Expense(
                title="Bilet miesieczny",
                amount="110.00",
                spent_on=date(2026, 6, 2),
                category=categories["Transport"],
                payment_method=methods["Przelew"],
            ),
            Expense(
                title="Kino",
                amount="38.00",
                spent_on=date(2026, 6, 3),
                category=categories["Rozrywka"],
                payment_method=methods["Karta"],
            ),
        ]
    )


def unseed_data(apps, schema_editor):
    apps.get_model("expenses", "Expense").objects.all().delete()
    apps.get_model("expenses", "PaymentMethod").objects.all().delete()
    apps.get_model("expenses", "Category").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]
