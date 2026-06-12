from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    color = models.CharField(max_length=20, default="#2563eb")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Expense(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    spent_on = models.DateField()
    note = models.CharField(max_length=250, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="expenses"
    )
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.PROTECT, related_name="expenses"
    )

    class Meta:
        ordering = ["-spent_on", "-id"]

    def __str__(self):
        return f"{self.title} - {self.amount} zl"
