using CheckDiePreise.Data.Models;
using Microsoft.EntityFrameworkCore;

namespace CheckDiePreise.Data.Services;

public class ProductService
{
    public ProductService(DataContext context)
    {
        _context = context;
    }

    private DataContext _context;

    public async Task<List<Product>> GetAllProductsAsync()
    {
        List<Product> products = await Task.FromResult(_context.Product.ToList());
        return products;
    }

    public async Task CreateProductAsync()
    {
        Product productToAdd = new Product
        {
            Name = "Erbsen",
            Price = 13,
        };

        _context.Add(productToAdd);
        Console.WriteLine("CreateProduct() wurde aufgerufen!");
        await _context.SaveChangesAsync();
    }

    public bool CanConnectToDatabase()
    {
        try
        {
            // Versucht, die Datenbankverbindung zu öffnen und die erste Tabelle abzufragen
            return _context.Database.CanConnect();
        }
        catch (Exception)
        {
            return false;
        }
    }
}

