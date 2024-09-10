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
            // Liste der Stores, die durchsucht werden sollen
            List<string> stores = searchStores
                .Where(kvp => kvp.Value)
                .Select(kvp => kvp.Key)
                .ToList();

            // Datenbankabfrage aufbauen, um die benötigten Daten zu laden, basierend auf den Stores
            IQueryable<ProductChange> query = _context.ProductChanges.AsQueryable();

            if (!searchAll)
            {
                query = query.Where(p => stores.Contains(p.Store));
            }

            // Hole die Produkte in eine Liste (kein Vorfilter für den Namen, da wir Fuzzy-Suche anwenden)
            List<ProductChange> products = await query.ToListAsync();

            // Parallelisiere die Fuzzy-Suche, um sie effizienter zu machen
            var filteredProducts = products
                .AsParallel()  // Parallele Verarbeitung
                .Where(p => Fuzz.Ratio(p.Name.ToLower(), productName.ToLower()) > 70) // Fuzzy-Suche (Schwelle bei 70)
                .ToList();

            // Gruppierung und Filterung in Speicher
            var groupedProducts = filteredProducts
                .AsParallel()  // Parallele Verarbeitung der Gruppierung
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
