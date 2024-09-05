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

        public async Task<Dictionary<string, Dictionary<string, List<ProductChange>>>> GetGroupedProductsAsync(bool searchAll, string trend, Dictionary<string, bool> searchStores)
        {

            IQueryable<ProductChange> query = _context.ProductChanges;

            List<string> stores = searchStores
                 .Where(kvp => kvp.Value)
                 .Select(kvp => kvp.Key)
                 .ToList();

            if (!searchAll)
            {
                query = query.Where(p => stores.Contains(p.Store));
            }

            //if (trend != "both")
            //{
            //    query = query.Where(p => p.Trend == trend);
            //}

            List<ProductChange> products = await query.ToListAsync();

            var groupedProducts = products
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
                                    // Filtere nur die Gruppen, deren letzten Eintrag den gewünschten Trend hat
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
                        // Filtere leere Gruppen heraus und sortiere alphabetisch nach Key
                        .Where(kvp => kvp.Value.Any())
                        .OrderBy(kvp => kvp.Key)
                        .ToDictionary(kvp => kvp.Key, kvp => kvp.Value)
                )
                // Filtere leere Stores heraus und sortiere alphabetisch nach Key
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
