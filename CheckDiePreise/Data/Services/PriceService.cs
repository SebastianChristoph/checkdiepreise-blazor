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
        private int thresholdPriceDifference = 60;

        public async Task<ProductChange?> GetRandomProductChangeWithDelayForDebug()
        {
            return await _context.ProductChanges
              .Where(p => p.PriceBefore != 0 && p.DifferencePercentage != null && p.DifferencePercentage != 0)
              .Where(p => p.DifferencePercentage < thresholdPriceDifference)
              .OrderByDescending(p => (double)p.DifferencePercentage)
              .FirstOrDefaultAsync();
        }
        public async Task<List<ProductChange>> GetYesterdaysProductChanges(string storeName)
        {
            if (storeName == "all")
            {
                return await _context.ProductChanges
               .Where(p => p.Date.Date == DateTime.UtcNow.Date.AddDays(-1) && (p.Difference != 0 || p.DifferenceBaseprice != 0))
               .ToListAsync();
            }

            return await _context.ProductChanges
               .Where(p => p.Date.Date == DateTime.UtcNow.Date.AddDays(-1) && (p.Difference != 0 || p.DifferenceBaseprice != 0) && p.Store == storeName)
               .ToListAsync();

        }

        public async Task<DailyReport?> GetYesterdaysDailyReportByStore(string store)
        {
            return await _context.DailyReports
                .Where(r => r.Store == store && r.Date.Date == DateTime.UtcNow.Date.AddDays(-1))
                .FirstOrDefaultAsync();
        }

        public async Task<ProductChange?> GetYesterdaysProductChangeMaxAsync()
        {
            return await _context.ProductChanges
             .Where(p => p.PriceBefore != 0 && p.DifferencePercentage != null && p.DifferencePercentage > 0 && p.DifferencePercentage < thresholdPriceDifference && p.Date.Date == DateTime.UtcNow.Date.AddDays(-1))
             .OrderByDescending(p => (double)p.DifferencePercentage)
             .FirstOrDefaultAsync();
        }

        public async Task<ProductChange?> GetYesterdaysProductChangeMinAsync()
        {
            return await _context.ProductChanges
             .Where(p => p.PriceBefore != 0 && p.DifferencePercentage != null && p.DifferencePercentage < 0 && p.DifferencePercentage > (thresholdPriceDifference*-1) && p.Date.Date == DateTime.UtcNow.Date.AddDays(-1))
             .OrderBy(p => (double)p.DifferencePercentage)
             .FirstOrDefaultAsync();
        }

        public async Task<Dictionary<string, List<StorePriceChange>>> GetStorePriceChangesByStoreAsync(string storeName)
        {

            var storePriceChanges = await Task.FromResult(_context.StorePriceChanges
                .Where(spc => spc.StoreName == storeName)
                .OrderBy(spc => spc.Category)
                .ThenBy(spc => spc.Date)
                .GroupBy(spc => spc.Category)
                .ToDictionary(g => g.Key, g => g.ToList()));

            return storePriceChanges;
        }

        public async Task<int> GetYesterdaysNewPriceChangesCountForStoreAsync(string store)
        {
            List<ProductChange> todaysPriceChanges = await Task.FromResult(_context.ProductChanges
                .Where(pc => pc.Store == store && pc.Date.Date == DateTime.UtcNow.Date.AddDays(-1))
                .ToList());
            return todaysPriceChanges.Count;
        }

        public async Task<List<ProductChange>> GetAllProductChangesOfProductAsync(string store, string identifier)
        {
            List<ProductChange> productChanges = await Task.FromResult(_context.ProductChanges
                .Where(p=> p.Store == store && p.Identifier == identifier)
                .OrderBy(p => p.Date)
                .ToList());
            return productChanges;
        }

        public async Task<Dictionary<string, Dictionary<string, List<ProductChange>>>> GetGroupedProductsAsync(string productName, bool searchAll, string trend, Dictionary<string, bool> searchStores)
        {
            int fuzzThreshold = 50;
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
                .Where(p => Fuzz.Ratio(p.Name.ToLower(), productName.ToLower()) > fuzzThreshold || p.Name.ToLower().Contains(productName.ToLower()) ||p.Identifier.Contains(productName))
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
