from django import forms

from expenses.models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["title", "amount", "spent_on", "category", "payment_method", "note"]
        labels = {
            "title": "Nazwa",
            "amount": "Kwota",
            "spent_on": "Data",
            "category": "Kategoria",
            "payment_method": "Metoda platnosci",
            "note": "Notatka",
        }
        widgets = {
            "title": forms.TextInput(attrs={"maxlength": 100, "required": True}),
            "amount": forms.NumberInput(
                attrs={"min": "0.01", "step": "0.01", "required": True}
            ),
            "spent_on": forms.DateInput(attrs={"type": "date", "required": True}),
            "note": forms.Textarea(attrs={"rows": 4, "maxlength": 250}),
        }
