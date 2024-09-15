using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Configuration;
using System.Globalization;

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
            foreach(var prodcutChange in _productChanges)
            {
                _chartData.Add(new DataItem
                {
                    Date = prodcutChange.Date,
                    Price = (double)prodcutChange.Price,
                });
            }
        }

        private static string FormatAsDouble(object value)
        {
            return ((double)value).ToString("N1", CultureInfo.CurrentCulture);
        }

        public class DataItem
        {
            public DateTime Date { get; set; }
            public double? Price { get; set; }
        }
    }
}
