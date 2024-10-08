using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;
using MudBlazor;
using Radzen.Blazor;
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

    public void AddProductToChart(string productName, string store, string identifier)
    {

        var productChanges = _productData[store][identifier];
        DateTime today = DateTime.Today;
        List<DataItem> dataItemList = [];

        // Anlegen eines DataItems mit Price = null für jeden Tag seit Startdatum
        for (DateTime date = productChanges[0].Date; date <= today; date = date.AddDays(1))
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
            var matchingProductChange = productChanges.FirstOrDefault(change => change.Date.ToString("dd.MM.yyyy") == dataItem.Date);

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

        if (_chartData.ContainsKey(productName)){
            _chartData.Remove(productName);
        }
        else
        {
            _chartData.Add(productName, dataItemList);
        }
       
        if (_identifierInChart.Contains(identifier)){
            _identifierInChart.Remove(identifier);
        }
        else
        {
            _identifierInChart.Add(identifier);
        }
    }

    private void DeleteAllSeriesInChart()
    {
        _chartData = [];
        _identifierInChart = [];
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
