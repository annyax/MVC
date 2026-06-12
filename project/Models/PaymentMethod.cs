using System.ComponentModel.DataAnnotations;

namespace MvcMovie.Models;

public class PaymentMethod
{
    public int Id { get; set; }

    [Required]
    [StringLength(60)]
    public string Name { get; set; } = string.Empty;

    public ICollection<Expense> Expenses { get; set; } = new List<Expense>();
}
