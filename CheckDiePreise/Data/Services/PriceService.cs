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

        public async Task<List<ProductChange>> GetRandomProductsAsync()
        {
            List<ProductChange> products = await _context.ProductChanges
                .Take(5)                      // 10 Einträge nehmen
                .ToListAsync();                // Asynchron abrufen

            return products;
        }

        public async Task<ProductChange> GetRandomPriceChangeAsync()
        {
            ProductChange product = await _context.ProductChanges.FirstOrDefaultAsync();
            return product;
        }


        public async Task<List<ProductChange>> GetTodaysProductChanges()
        {
            List<ProductChange> products = await _context.ProductChanges
                .Where(p => p.Date == DateTime.Today)
                .ToListAsync();

            return products;
        }

        public async Task<ProductChange> GetTodaysProductChangeMaxAsync()
        {
            List<ProductChange> products = await _context.ProductChanges
                .Where(p => p.Date == DateTime.Today)
                .ToListAsync();  // Datenbankabruf ohne Sortierung

            ProductChange product = products
                .OrderByDescending(p => p.Difference)  // Sortierung auf der Clientseite
                .FirstOrDefault();  // Das größte Element auswählen

            return product;
        }

        public async Task<ProductChange> GetTodaysProductChangeMinAsync()
        {

            List<ProductChange> products = await _context.ProductChanges
                .Where(p => p.Date == DateTime.Today)
                .ToListAsync();  // Datenbankabruf ohne Sortierung

            ProductChange product = products
                .OrderBy(p => p.Difference)
                .FirstOrDefault();  // Das größte Element auswählen

            return product;
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
            string sql = query.ToQueryString();

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
                        .GroupBy(p => p.Identifier)
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
