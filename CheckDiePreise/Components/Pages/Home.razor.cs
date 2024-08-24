using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;

namespace CheckDiePreise.Components.Pages
{
    public partial class Home
    {
        private string? _connectionString;
        private List<Product> _products = [];
        private bool _canConnect;
        private string _status = "kein Status";
        
        [Inject]
        private ProductService ProductService{ get; set; } = null!;

        [Inject] IConfiguration Configuration { get; set; } = null!;

        protected override async Task OnInitializedAsync()
        {
            _products = await ProductService.GetAllProductsAsync();
            _connectionString = Configuration.GetConnectionString("DefaultConnection");
            _canConnect = ProductService.CanConnectToDatabase();
        }

        private async Task CreateProduct()
        {
            await ProductService.CreateProductAsync();
            _status = "hinzugef�gt";
            _products = await ProductService.GetAllProductsAsync();
        }

    }
}