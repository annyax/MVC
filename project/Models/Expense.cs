using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MvcMovie.Models;

public class Expense
{
    public int Id { get; set; }

    [Required(ErrorMessage = "Nazwa wydatku jest wymagana.")]
    [StringLength(100)]
    public string Title { get; set; } = string.Empty;

    [Required]
    [Range(0.01, 1000000, ErrorMessage = "Kwota musi byc wieksza lub rowna 0.01.")]
    [Column(TypeName = "decimal(10, 2)")]
    public decimal Amount { get; set; }

    [Required]
    [DataType(DataType.Date)]
    public DateTime SpentOn { get; set; } = DateTime.Today;

    [StringLength(250)]
    public string? Note { get; set; }

    [Display(Name = "Kategoria")]
    public int CategoryId { get; set; }
    public Category? Category { get; set; }

    [Display(Name = "Metoda platnosci")]
    public int PaymentMethodId { get; set; }
    public PaymentMethod? PaymentMethod { get; set; }
}
