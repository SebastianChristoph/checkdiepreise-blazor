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
        private List<DataItem> _chartDataBaseprice = [];
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
            DateTime today = DateTime.Today;
            List<DataItem> dataItemList = [];
            for (DateTime date = _productChanges[0].Date; date <= today; date = date.AddDays(1))
            {

                DataItem dataItem = new DataItem
                {
                    Date = date.ToString("dd.MM.yyyy"),
                    Price = 0
                };

                if (!dataItemList.Contains(dataItem))
                {
                    dataItemList.Add(dataItem);
                }

            }

            decimal lastPrice = 0;
            foreach (var dataItem in dataItemList)
            {
                var matchingProductChange = _productChanges.FirstOrDefault(change => change.Date.ToString("dd.MM.yyyy") == dataItem.Date);

                if (matchingProductChange != null)
                {
                    // Preis des ProductChange setzen
                    lastPrice = matchingProductChange.Price;
                    dataItem.Price = (double)matchingProductChange.Price;
                }
                else
                {
                    dataItem.Price = (double?)lastPrice;
                }
            }

            _chartData = dataItemList;


            List<DataItem> dataItemListBasePrice = [];
            for (DateTime date = _productChanges[0].Date; date <= today; date = date.AddDays(1))
            {

                DataItem dataItem = new DataItem
                {
                    Date = date.ToString("dd.MM.yyyy"),
                    Price = 0
                };

                if (!dataItemListBasePrice.Contains(dataItem))
                {
                    dataItemListBasePrice.Add(dataItem);
                }

            }

            decimal lastBaseprice = 0;
            foreach (var dataItem in dataItemListBasePrice)
            {
                var matchingProductChange = _productChanges.FirstOrDefault(change => change.Date.ToString("dd.MM.yyyy") == dataItem.Date);

                if (matchingProductChange != null)
                {
                    // Preis des ProductChange setzen
                    lastPrice = matchingProductChange.Baseprice;
                    dataItem.Price = (double)matchingProductChange.Baseprice;
                }
                else
                {
                    dataItem.Price = (double?)lastPrice;
                }
            }

            _chartDataBaseprice = dataItemList;
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

        public double GetLatestBasepriceChange(List<ProductChange> priceChanges)
        {
            // Suche das Element mit dem letzten Datum
            var lastPriceChange = priceChanges
                .OrderByDescending(spc => spc.Date) // Sortiere absteigend nach Datum
                .FirstOrDefault();                  // Nimm das erste Element (nähestes zu heute)
            if (lastPriceChange != null)
            {
                return (double)lastPriceChange.Baseprice;
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
