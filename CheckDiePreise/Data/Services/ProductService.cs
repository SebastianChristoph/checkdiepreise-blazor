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
        List<Product> products = await Task.FromResult(_context.Products.ToList());
        return products;
    }
}

