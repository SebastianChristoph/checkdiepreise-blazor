using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;
using System.Globalization;

namespace CheckDiePreise.Components.Pages
{
    public partial class StoreAnalysis
    {
        private List<StorePriceChange>? _storePriceChanges;
        private Dictionary<string, List<DataItem>> _chartData = [];
        private string _store = string.Empty;
        private bool _displayUnit = true;
        private List<string> _availableStores = [];
        private bool _showSpinner = false;

        [Inject] PriceService PriceService { get; set; } = null!;

        [Inject] IConfiguration Configuration { get; set; } = null!;

        protected override async Task OnInitializedAsync()
        {
            base.OnInitialized();
            _availableStores = Configuration.GetValue<string>("Stores").Split(",").ToList();
            _availableStores.Sort();
        }


        private async Task DrawChart(string storeName = "")
        {
            _showSpinner = true;
            StateHasChanged();
            await Task.Delay(1);

            _chartData = [];
            _store = storeName;
            var storedata = await PriceService.GetStorePriceChangesByStoreAsync(_store);
           

            foreach (KeyValuePair<string, List<StorePriceChange>> category in storedata)
            {
                List<DataItem> data = [];
                bool foundToday = false;
                double lastPrice = 0;

                foreach (var entry in category.Value)
                {
                    if(entry.Date == DateTime.UtcNow.Date)
                    {
                        foundToday = true;
                    }

                    data.Add(new DataItem
                    {
                        Date = entry.Date.ToString("dd.MM.yyyy"),
                        Price = _displayUnit ? (double)entry.Price : (double)entry.Baseprice,
                    });

                }


                if (!foundToday)
                {

                    data.Add(new DataItem
                    {
                        Date = DateTime.UtcNow.Date.ToString(),
                        Price = GetLatestPriceChange(category.Value),
                    });
                }

                _chartData.Add(category.Key, data);
            }
            _showSpinner = false;
            StateHasChanged();
        }
        public double GetLatestPriceChange(List<StorePriceChange> storePriceChanges)
        {
            // Suche das Element mit dem letzten Datum
            var lastPriceChange =  storePriceChanges
                .OrderByDescending(spc => spc.Date) // Sortiere absteigend nach Datum
                .FirstOrDefault();                  // Nimm das erste Element (nähestes zu heute)
            if (lastPriceChange != null)
            {
                return _displayUnit ? (double)lastPriceChange.Price : (double)lastPriceChange.Baseprice;
            }
            else return 0;
        }

        private void SetPrice(bool status)
        {
            _displayUnit = status;
            DrawChart(_store);
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