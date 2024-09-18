using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Configuration;
using System.Globalization;
using static System.Runtime.InteropServices.JavaScript.JSType;

namespace CheckDiePreise.Components.Pages
{
    public partial class ProductDetail
    {

        private List<ProductChange> _productChanges;
        private List<DataItem> _chartData = [];
        [Parameter] public string? Store { get; set; }
        [Parameter] public string? Name { get; set; }
        [Parameter] public string? Identifier { get; set; }

        [Inject]
        private PriceService PriceService { get; set; } = null!;

        protected override async Task OnInitializedAsync()
        {
            base.OnInitialized();
            _productChanges = await PriceService.GetAllProductChangesOfProductAsync(Store, Identifier);
            DrawChart();
        }

        private void DrawChart()
        {
            bool foundToday = false;
            double lastPrice = 0;

            foreach (var prodcutChange in _productChanges)
            {
                if (prodcutChange.Date == DateTime.UtcNow.Date)
                {
                    foundToday = true;
                }

                _chartData.Add(new DataItem
                {
                    Date = prodcutChange.Date.ToString("dd.MM.yyyy"),
                    Price = (double)prodcutChange.Price,
                });
            }
            if (!foundToday)
            {

                _chartData.Add(new DataItem
                {
                    Date = DateTime.UtcNow.Date.ToString("dd.MM.yyyy"),
                    Price = GetLatestPriceChange(_productChanges),
                });
            }
        }

        public double GetLatestPriceChange(List<ProductChange> priceChanges)
        {
            // Suche das Element mit dem letzten Datum
            var lastPriceChange = priceChanges
                .OrderByDescending(spc => spc.Date) // Sortiere absteigend nach Datum
                .FirstOrDefault();                  // Nimm das erste Element (nähestes zu heute)
            if (lastPriceChange != null)
            {
                return (double)lastPriceChange.Price;
            }
            else return 0;
        }

        private static string FormatAsDouble(object value)
        {
            return ((double)value).ToString("N1", CultureInfo.CurrentCulture);
        }

        public class DataItem
        {
            public string Date { get; set; }
            public double? Price { get; set; }
        }
    }
}
