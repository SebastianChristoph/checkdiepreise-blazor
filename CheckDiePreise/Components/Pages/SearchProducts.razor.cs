using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;

namespace CheckDiePreise.Components.Pages;

public partial class SearchProducts
{
    private string _productName;
    private string _productStore;
    private List<ProductChange> _productChanges;
    private List<ProductChange> _allProducts;
    private bool _isSearching = false;
    string[] headings = { "ID", "Name", "Date", "Identifier", "Price", "Store", "Category" };

    [Inject]
    private PriceService PriceService { get; set; } = null!;

    private async Task SearchProductChanges()
    {
        _isSearching = true;
        _productChanges = await PriceService.SearchProductChanges(_productName);
        _isSearching = false;
    }

    private async Task GetAllProducts()
    {
        _allProducts = await PriceService.GetAllProductsAsync();
        StateHasChanged();
    }
}
