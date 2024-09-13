using CheckDiePreise.Data.Models;
using Microsoft.EntityFrameworkCore;
using FuzzySharp;

namespace CheckDiePreise.Data.Services
{
    public class PriceService
    {
        public PriceService(DataContext context)
        {
            _context = context;
        }

        private DataContext _context;

        public async Task<List<StorePriceChange>> GetStorePriceChangesByStore(string storeName)
        {
            List<StorePriceChange> storePricesChanges = await Task.FromResult(_context.StorePriceChanges
                .Where(spc => spc.StoreName == storeName)
                .OrderBy(spc => spc.Category)
                .ThenBy(spc => spc.Date)
                .ToList());
            return storePricesChanges;
        }

        public async Task<Dictionary<string, List<StorePriceChange>>> GetStorePriceChangesByStoreAsync(string storeName)
        {
            // Hole die Preisänderungen und gruppiere sie nach Kategorie
            var storePriceChanges = await Task.FromResult(_context.StorePriceChanges
                .Where(spc => spc.StoreName == storeName)
                .OrderBy(spc => spc.Category)
                .ThenBy(spc => spc.Date)
                .GroupBy(spc => spc.Category)
                .ToDictionary(g => g.Key, g => g.ToList()));

            return storePriceChanges;
        }


        public async Task<List<ProductChange>> GetAllProductsAsync()
        {
            List<ProductChange> products = await Task.FromResult(_context.ProductChanges.ToList());
            return products;
        }

        public async Task<DailyStats> GetLastDailyStat()
        {
            DailyStats dailyStat = await _context.DailyStats
                                          .OrderByDescending(d => d.Date)
                                          .FirstOrDefaultAsync();
            return dailyStat;
        }

        public async Task<List<ProductChange>> GetAllProductChangesOfProductAsync(string store, string identifier)
        {
            List<ProductChange> productChanges = await Task.FromResult(_context.ProductChanges
                .Where(p=> p.Store == store && p.Identifier == identifier)
                .ToList());
            return productChanges;
        }

        public async Task<Dictionary<string, Dictionary<string, List<ProductChange>>>> GetGroupedProductsAsync(string productName, bool searchAll, string trend, Dictionary<string, bool> searchStores)
        {
            List<string> stores = searchStores
                .Where(kvp => kvp.Value)
                .Select(kvp => kvp.Key)
                .ToList();

            IQueryable<ProductChange> query = _context.ProductChanges.AsQueryable();

            if (!searchAll)
            {
                query = query.Where(p => stores.Contains(p.Store));
            }

            List<ProductChange> products = await query.ToListAsync();

            var filteredProducts = products
                .AsParallel()
                .Where(p => Fuzz.Ratio(p.Name.ToLower(), productName.ToLower()) > 50)
                .ToList();

            var groupedProducts = filteredProducts
                .AsParallel()
                .GroupBy(p => p.Store)
                .ToDictionary(
                    storeGroup => storeGroup.Key,
                    storeGroup => storeGroup
                        .GroupBy(p => p.Name)
                        .ToDictionary(
                            nameGroup => nameGroup.Key,
                            nameGroup =>
                            {
                                var orderedProducts = nameGroup.OrderBy(p => p.Date).ToList();
                                if (trend != "both")
                                {
                                    if (orderedProducts.Last().Trend == trend)
                                    {
                                        return orderedProducts;
                                    }
                                    else
                                    {
                                        return new List<ProductChange>();
                                    }
                                }
                                return orderedProducts;
                            }
                        )
                        .Where(kvp => kvp.Value.Any())
                        .OrderBy(kvp => kvp.Key)
                        .ToDictionary(kvp => kvp.Key, kvp => kvp.Value)
                )
                .Where(storeGroup => storeGroup.Value.Any())
                .OrderBy(storeGroup => storeGroup.Key)
                .ToDictionary(kvp => kvp.Key, kvp => kvp.Value);

            return groupedProducts;
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
