using CheckDiePreise.Data.Models;
using Microsoft.EntityFrameworkCore;

namespace CheckDiePreise.Data.Services
{
    public class PriceService
    {
        public PriceService(DataContext context)
        {
            _context = context;
        }

        private DataContext _context;

        public async Task<List<ProductChange>> GetAllProductsAsync()
        {
            List<ProductChange> products = await Task.FromResult(_context.ProductChanges.ToList());
            return products;
        }

        public async Task<List<ProductChange>> SearchProductChanges(string productName)
        {
            List<ProductChange> products = await _context.ProductChanges
                .Where(p => p.Name.ToLower().Contains(productName.ToLower()))
                .ToListAsync();

            return products;
        }


        public bool CanConnectToDatabase()
        {
            try
            {
                return _context.Database.CanConnect();
            }
            catch (Exception)
            {
                return false;
            }
        }

    }
}
