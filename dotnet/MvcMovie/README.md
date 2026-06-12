# Budzet Domowy - ASP.NET Core MVC

Projekt zaliczeniowy wykonany w ASP.NET Core MVC z widokami Razor `.cshtml`.

## Funkcjonalnosci

- lista wydatkow w tabeli,
- dodawanie wydatkow,
- edycja wydatkow,
- usuwanie wydatkow,
- widok szczegolow pojedynczego wydatku,
- wyszukiwanie po nazwie,
- filtrowanie po kategorii i metodzie platnosci,
- walidacja kwoty, nazwy i dlugosci tekstu,
- modele powiazane relacjami jeden-do-wielu.

## MVC

- Model: `Models/Expense.cs`, `Models/Category.cs`, `Models/PaymentMethod.cs`
- Controller: `Controllers/ExpensesController.cs`
- View: `Views/Expenses/*.cshtml`

## Uruchomienie

```bash
cd dotnet/MvcMovie
dotnet run
```

Aplikacja uruchamia sie jako system Budzet Domowy. Baza SQLite `HomeBudget.db` tworzy sie automatycznie przy starcie aplikacji.
