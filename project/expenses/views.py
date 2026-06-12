from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from expenses.forms import ExpenseForm
from expenses.models import Category, Expense, PaymentMethod


def expense_list(request):
    expenses = Expense.objects.select_related("category", "payment_method")
    search = request.GET.get("search", "").strip()
    category_id = request.GET.get("category_id", "").strip()
    payment_method_id = request.GET.get("payment_method_id", "").strip()

    if search:
        expenses = expenses.filter(title__icontains=search)
    if category_id:
        expenses = expenses.filter(category_id=category_id)
    if payment_method_id:
        expenses = expenses.filter(payment_method_id=payment_method_id)

    total = expenses.aggregate(total=Sum("amount"))["total"] or 0

    return render(
        request,
        "expenses/index.html",
        {
            "expenses": expenses,
            "categories": Category.objects.all(),
            "payment_methods": PaymentMethod.objects.all(),
            "total": total,
            "filters": request.GET,
        },
    )


def expense_detail(request, pk):
    expense = get_object_or_404(
        Expense.objects.select_related("category", "payment_method"), pk=pk
    )
    return render(request, "expenses/details.html", {"expense": expense})


def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Wydatek zostal dodany.")
            return redirect("expense_list")
    else:
        form = ExpenseForm()

    return render(request, "expenses/form.html", {"form": form, "is_edit": False})


def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Wydatek zostal zaktualizowany.")
            return redirect("expense_detail", pk=expense.pk)
    else:
        form = ExpenseForm(instance=expense)

    return render(request, "expenses/form.html", {"form": form, "is_edit": True})


def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Wydatek zostal usuniety.")
    return redirect("expense_list")
