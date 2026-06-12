using System.ComponentModel.DataAnnotations;

namespace MvcMovie.Models;

public class Category
{
    public int Id { get; set; }

    [Required]
    [StringLength(60)]
    public string Name { get; set; } = string.Empty;

    [Required]
    [StringLength(20)]
    public string Color { get; set; } = "#2563eb";

    public ICollection<Expense> Expenses { get; set; } = new List<Expense>();
}
