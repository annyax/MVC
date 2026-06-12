from datetime import date

from django.test import TestCase
from django.urls import reverse

from expenses.models import Category, Expense, PaymentMethod


class ExpenseViewsTests(TestCase):
    def setUp(self):
        Expense.objects.all().delete()
        self.category = Category.objects.create(name="Test Jedzenie", color="#16a34a")
        self.payment_method = PaymentMethod.objects.create(name="Test Karta")
        Expense.objects.create(
            title="Zakupy spozywcze",
            amount="84.50",
            spent_on=date(2026, 6, 1),
            category=self.category,
            payment_method=self.payment_method,
        )
        Expense.objects.create(
            title="Kino",
            amount="38.00",
            spent_on=date(2026, 6, 3),
            category=self.category,
            payment_method=self.payment_method,
        )

    def test_index_loads_expenses(self):
        response = self.client.get(reverse("expense_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Zakupy spozywcze")

    def test_search_filters_expenses(self):
        response = self.client.get(reverse("expense_list"), {"search": "Kino"})

        self.assertContains(response, "Kino")
        self.assertNotContains(response, "Zakupy spozywcze")

    def test_create_expense_requires_positive_amount(self):
        response = self.client.post(
            reverse("expense_create"),
            {
                "title": "Test",
                "amount": "-1",
                "spent_on": "2026-06-07",
                "category": self.category.id,
                "payment_method": self.payment_method.id,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "większa lub równa 0.01")
