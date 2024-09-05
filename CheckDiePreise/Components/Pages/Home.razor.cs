using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Forms;

namespace CheckDiePreise.Components.Pages
{
    public partial class Home
    {
        private string? _connectionString;
        private List<ProductChange> _products = [];
        private bool _canConnect;
        private string _usedDb = string.Empty;
        
        [Inject]
        private PriceService PriceService{ get; set; } = null!;

        [Inject] IConfiguration Configuration { get; set; } = null!;

        protected override void OnInitialized()
        {
            base.OnInitialized();
            _connectionString = Configuration.GetConnectionString("DefaultConnection");
            _canConnect = PriceService.CanConnectToDatabase();
            _usedDb = Configuration.GetValue<string>("UseDb");
        }

       

    }
}