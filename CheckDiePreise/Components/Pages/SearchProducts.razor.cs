using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;
using MudBlazor;
using Radzen.Blazor;
using Radzen.Blazor.Rendering;
using System.Globalization;

namespace CheckDiePreise.Components.Pages;

public partial class SearchProducts
{
    private string _productName = string.Empty;
    private List<string> _availableStores = [];
    private Dictionary<string, bool> _searchStores = [];
    private bool _isSearching = false;
    private bool _searchAll = true;
    private string _searchTrend = "both";
    string[] headings = {"Name", "Date", "Identifier", "Price", "Store", "Category" };
    private Dictionary<string, Dictionary<string, List<ProductChange>>>? _productData;
    public Dictionary<string, List<DataItem>> _chartData = new Dictionary<string, List<DataItem>>();
    Interpolation interpolation = Interpolation.Step;

    private List<string> _identifierInChart = [];


    private List<DateTime> allDatesInChart = [];

    private Dictionary<string, List<ProductChange>> allSeriesInChart = [];

    [Parameter] public string Product { get; set; }

    [Inject] private PriceService PriceService { get; set; } = null!;
    [Inject] IConfiguration Configuration { get; set; } = null!;
    [Inject] ISnackbar Snackbar { get; set; } = null!;

    protected override void OnInitialized()
    {
        base.OnInitialized();
        _availableStores = Configuration.GetValue<string>("Stores").Split(",").ToList();
        foreach (string store in _availableStores)
        {
            _searchStores.Add(store, false);
        }

        if (Product is not null)
        {
            _productName = Product;
            SearchProductChanges();
        }
    }

    private async Task SearchProductChanges()
    {
        if (_productName.Length <= 2)
        {
            Snackbar.Add("Bitte geben Sie mehr als 2 Buchstaben als Produktnamen ein!", Severity.Warning);
            return;
        }

        DeleteAllSeriesInChart();
        _productData = [];
        _isSearching = true;
        StateHasChanged();

        await Task.Delay(1);

        _productData = await PriceService.GetGroupedProductsAsync(_productName, _searchAll, _searchTrend, _searchStores);
        _isSearching = false;
        StateHasChanged();
    }

    public void AddChartData(string store, string productName, string identifier)
    {

        var productChanges = _productData[store][productName];
        if (!allSeriesInChart.ContainsKey(productName))
        {
            allSeriesInChart.Add(productName, productChanges);
            _identifierInChart.Add(identifier);
        }
        else
        {
            allSeriesInChart.Remove(productName);
            _identifierInChart.Remove(identifier);
        }
        ReOrderChartData(productChanges);
    }

    private void ReOrderChartData(List<ProductChange> newDataSet)
    {
        foreach (var productChange in newDataSet)
        {

            if (!allDatesInChart.Contains(productChange.Date))
            {
                allDatesInChart.Add(productChange.Date);
            }
        }
        allDatesInChart.Sort();
        ReDrawChart();
    }

    private void ReDrawChart()
    {
        _chartData = new Dictionary<string, List<DataItem>>();
        foreach (KeyValuePair<string, List<ProductChange>> serie in allSeriesInChart)
        {
            List<DataItem> serieData = [];
            foreach(DateTime date in allDatesInChart) {

                double? price = null;
                // Suche nach einem ProductChange, dessen Datum mit dem aktuellen Datum übereinstimmt
                var matchingProductChange = serie.Value.FirstOrDefault(pc => pc.Date == date);

                if (matchingProductChange != null)
                {
                    // Wenn eine Übereinstimmung gefunden wurde, setze den Preis
                    price = (double)matchingProductChange.Price;
                    serieData.Add(new DataItem
                    {
                        Date = date,
                        Price = price,
                    });
                }
            }

            _chartData.Add(serie.Key, serieData);
        }
    }

    private void DeleteAllSeriesInChart()
    {
        allSeriesInChart = [];
        _identifierInChart = [];
        allDatesInChart = [];
        ReDrawChart();
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
