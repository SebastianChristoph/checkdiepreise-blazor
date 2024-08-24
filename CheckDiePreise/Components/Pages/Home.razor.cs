using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;

namespace CheckDiePreise.Components.Pages
{
    public partial class Home
    {
        private List<Product> _products = [];
        [Inject]
        private ProductService ProductService{ get; set; } = null!;

        protected override async Task OnInitializedAsync()
        {
            _products = await ProductService.GetAllProductsAsync();
        }

    }
}