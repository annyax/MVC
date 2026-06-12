using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using MvcMovie.Data;
using System;
using System.Linq;

namespace MvcMovie.Models;

public static class SeedData
{
    public static void Initialize(IServiceProvider serviceProvider)
    {
        using (var context = new MvcMovieContext(
            serviceProvider.GetRequiredService<
                DbContextOptions<MvcMovieContext>>()))
        {
            context.Database.EnsureCreated();

            if (!context.Categories.Any())
            {
                var categories = new[]
                {
                    new Category { Name = "Jedzenie", Color = "#16a34a" },
                    new Category { Name = "Transport", Color = "#2563eb" },
                    new Category { Name = "Dom", Color = "#ea580c" },
                    new Category { Name = "Rozrywka", Color = "#9333ea" }
                };

                var methods = new[]
                {
                    new PaymentMethod { Name = "Karta" },
                    new PaymentMethod { Name = "Gotowka" },
                    new PaymentMethod { Name = "Przelew" }
                };

                context.Categories.AddRange(categories);
                context.PaymentMethods.AddRange(methods);
                context.SaveChanges();

                context.Expenses.AddRange(
                    new Expense
                    {
                        Title = "Zakupy spozywcze",
                        Amount = 84.50M,
                        SpentOn = new DateTime(2026, 6, 1),
                        CategoryId = categories[0].Id,
                        PaymentMethodId = methods[0].Id,
                        Note = "Tygodniowe zakupy"
                    },
                    new Expense
                    {
                        Title = "Bilet miesieczny",
                        Amount = 110.00M,
                        SpentOn = new DateTime(2026, 6, 2),
                        CategoryId = categories[1].Id,
                        PaymentMethodId = methods[2].Id
                    },
                    new Expense
                    {
                        Title = "Kino",
                        Amount = 38.00M,
                        SpentOn = new DateTime(2026, 6, 3),
                        CategoryId = categories[3].Id,
                        PaymentMethodId = methods[0].Id
                    }
                );
                context.SaveChanges();
            }

            // Look for any movies.
            if (context.Movie.Any())
            {
                return;   // DB has been seeded
            }
            context.Movie.AddRange(
                new Movie
                {
                    Title = "When Harry Met Sally",
                    ReleaseDate = DateTime.Parse("1989-2-12"),
                    Genre = "Romantic Comedy",
                    Rating = "R",
                    Price = 7.99M
                },
                new Movie
                {
                    Title = "Ghostbusters ",
                    ReleaseDate = DateTime.Parse("1984-3-13"),
                    Genre = "Comedy",
                    Rating = "R",
                    Price = 8.99M
                },
                new Movie
                {
                    Title = "Ghostbusters 2",
                    ReleaseDate = DateTime.Parse("1986-2-23"),
                    Genre = "Comedy",
                    Rating = "R",
                    Price = 9.99M
                },
                new Movie
                {
                    Title = "Rio Bravo",
                    ReleaseDate = DateTime.Parse("1959-4-15"),
                    Genre = "Western",
                    Rating = "R",
                    Price = 3.99M
                }
            );
            context.SaveChanges();
        }
    }
}
