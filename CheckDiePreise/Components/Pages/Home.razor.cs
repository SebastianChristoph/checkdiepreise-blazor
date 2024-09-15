using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Forms;

namespace CheckDiePreise.Components.Pages
{
    public partial class Home
    {
        private string? _connectionString;
        private ProductChange _maxChange;
        private ProductChange _minChange; 
        private bool _canConnect;
        private string _usedDb = string.Empty;
        private string _hrefMinProduct;
        private string _hrefMaxProduct;

        [Inject]
        private PriceService PriceService{ get; set; } = null!;

        [Inject] IConfiguration Configuration { get; set; } = null!;

        protected override async Task OnInitializedAsync()
        {
            base.OnInitialized();
            _connectionString = Configuration.GetConnectionString("DefaultConnection");
            _canConnect = PriceService.CanConnectToDatabase();
            _usedDb = Configuration.GetValue<string>("UseDb");
            _maxChange = await PriceService.GetTodaysProductChangeMaxAsync();
            _minChange = await PriceService.GetTodaysProductChangeMinAsync();

            if(_maxChange is null)
            {
                _maxChange = await PriceService.GetRandomPriceChangeAsync();
            }


            if (_minChange is null)
            {
                _minChange = await PriceService.GetRandomPriceChangeAsync();
            }

            if (_minChange is not null && _maxChange is not null)
            {
                _hrefMinProduct = $"/product/{_minChange.Store}/{_minChange.Name}-{_minChange.Identifier}";
                _hrefMaxProduct = $"/product/{_maxChange.Store}/{_maxChange.Name}-{_maxChange.Identifier}";
            }
        }
    }
}