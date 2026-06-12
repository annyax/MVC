from django.contrib import admin

from expenses.models import Category, Expense, PaymentMethod


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
    search_fields = ("name",)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "spent_on", "category", "payment_method")
    list_filter = ("category", "payment_method", "spent_on")
    search_fields = ("title", "note")
