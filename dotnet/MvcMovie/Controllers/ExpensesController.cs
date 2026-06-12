using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using MvcMovie.Data;
using MvcMovie.Models;

namespace MvcMovie.Controllers;

public class ExpensesController : Controller
{
    private readonly MvcMovieContext _context;

    public ExpensesController(MvcMovieContext context)
    {
        _context = context;
    }

    public async Task<IActionResult> Index(string? searchString, int? categoryId, int? paymentMethodId)
    {
        var expenses = _context.Expenses
            .Include(e => e.Category)
            .Include(e => e.PaymentMethod)
            .AsQueryable();

        if (!string.IsNullOrWhiteSpace(searchString))
        {
            expenses = expenses.Where(e => e.Title.Contains(searchString));
        }

        if (categoryId.HasValue)
        {
            expenses = expenses.Where(e => e.CategoryId == categoryId.Value);
        }

        if (paymentMethodId.HasValue)
        {
            expenses = expenses.Where(e => e.PaymentMethodId == paymentMethodId.Value);
        }

        var list = await expenses
            .OrderByDescending(e => e.SpentOn)
            .ThenByDescending(e => e.Id)
            .ToListAsync();

        var viewModel = new ExpenseIndexViewModel
        {
            Expenses = list,
            Categories = new SelectList(await _context.Categories.OrderBy(c => c.Name).ToListAsync(), "Id", "Name"),
            PaymentMethods = new SelectList(await _context.PaymentMethods.OrderBy(p => p.Name).ToListAsync(), "Id", "Name"),
            SearchString = searchString,
            CategoryId = categoryId,
            PaymentMethodId = paymentMethodId,
            Total = list.Sum(e => e.Amount)
        };

        return View(viewModel);
    }

    public async Task<IActionResult> Details(int? id)
    {
        if (id == null)
        {
            return NotFound();
        }

        var expense = await _context.Expenses
            .Include(e => e.Category)
            .Include(e => e.PaymentMethod)
            .FirstOrDefaultAsync(e => e.Id == id);

        return expense == null ? NotFound() : View(expense);
    }

    public async Task<IActionResult> Create()
    {
        await PopulateSelectLists();
        return View();
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create([Bind("Title,Amount,SpentOn,Note,CategoryId,PaymentMethodId")] Expense expense)
    {
        if (ModelState.IsValid)
        {
            _context.Add(expense);
            await _context.SaveChangesAsync();
            return RedirectToAction(nameof(Index));
        }

        await PopulateSelectLists(expense.CategoryId, expense.PaymentMethodId);
        return View(expense);
    }

    public async Task<IActionResult> Edit(int? id)
    {
        if (id == null)
        {
            return NotFound();
        }

        var expense = await _context.Expenses.FindAsync(id);
        if (expense == null)
        {
            return NotFound();
        }

        await PopulateSelectLists(expense.CategoryId, expense.PaymentMethodId);
        return View(expense);
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(int id, [Bind("Id,Title,Amount,SpentOn,Note,CategoryId,PaymentMethodId")] Expense expense)
    {
        if (id != expense.Id)
        {
            return NotFound();
        }

        if (ModelState.IsValid)
        {
            _context.Update(expense);
            await _context.SaveChangesAsync();
            return RedirectToAction(nameof(Details), new { id = expense.Id });
        }

        await PopulateSelectLists(expense.CategoryId, expense.PaymentMethodId);
        return View(expense);
    }

    public async Task<IActionResult> Delete(int? id)
    {
        if (id == null)
        {
            return NotFound();
        }

        var expense = await _context.Expenses
            .Include(e => e.Category)
            .Include(e => e.PaymentMethod)
            .FirstOrDefaultAsync(e => e.Id == id);

        return expense == null ? NotFound() : View(expense);
    }

    [HttpPost, ActionName("Delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> DeleteConfirmed(int id)
    {
        var expense = await _context.Expenses.FindAsync(id);
        if (expense != null)
        {
            _context.Expenses.Remove(expense);
            await _context.SaveChangesAsync();
        }

        return RedirectToAction(nameof(Index));
    }

    private async Task PopulateSelectLists(int? categoryId = null, int? paymentMethodId = null)
    {
        ViewData["CategoryId"] = new SelectList(await _context.Categories.OrderBy(c => c.Name).ToListAsync(), "Id", "Name", categoryId);
        ViewData["PaymentMethodId"] = new SelectList(await _context.PaymentMethods.OrderBy(p => p.Name).ToListAsync(), "Id", "Name", paymentMethodId);
    }
}
