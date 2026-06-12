using Microsoft.AspNetCore.Mvc.Rendering;

namespace MvcMovie.Models;

public class ExpenseIndexViewModel
{
    public List<Expense> Expenses { get; set; } = new();
    public SelectList? Categories { get; set; }
    public SelectList? PaymentMethods { get; set; }
    public string? SearchString { get; set; }
    public int? CategoryId { get; set; }
    public int? PaymentMethodId { get; set; }
    public decimal Total { get; set; }
}
