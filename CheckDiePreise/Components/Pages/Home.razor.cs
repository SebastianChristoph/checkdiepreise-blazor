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
            _connectionString = Configuration.GetConnectionString("DefaultConnection");
            _canConnect = ProductService.CanConnectToDatabase();
            if (_canConnect)
            {
                _products = await ProductService.GetAllProductsAsync();
            }
        }

        private async Task CreateProduct()
        {
            await ProductService.CreateProductAsync();
            _status = "hinzugefügt";
            _products = await ProductService.GetAllProductsAsync();
        }

    }
}