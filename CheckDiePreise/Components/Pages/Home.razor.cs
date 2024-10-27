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
        private List<string> _availableStores = [];
        private bool _showSpinner = false;

        [Inject]
        private PriceService PriceService{ get; set; } = null!;

        [Inject] IConfiguration Configuration { get; set; } = null!;

        protected override async Task OnInitializedAsync()
        {
            base.OnInitialized();
            _connectionString = Configuration.GetConnectionString("DefaultConnection");
            _canConnect = PriceService.CanConnectToDatabase();
            _availableStores = Configuration.GetValue<string>("Stores").Split(",").ToList();
            _usedDb = Configuration.GetValue<string>("UseDb");

            _showSpinner = true;
            StateHasChanged();
            await Task.Delay(1);
        //#if DEBUG
        //            _minChange = await PriceService.GetRandomProductChangeWithDelayForDebug();
        //            _maxChange = await PriceService.GetRandomProductChangeWithDelayForDebug();
        //            _showSpinner = false;
        //            StateHasChanged();
        //            return;
        //#endif

            _maxChange = await PriceService.GetYesterdaysProductChangeMaxAsync();
            _minChange = await PriceService.GetYesterdaysProductChangeMinAsync();

            if (_minChange is not null)
            {
                _hrefMinProduct = $"/product/{_minChange.Store}/{_minChange.Name}-{_minChange.Identifier}";
            }

            if (_maxChange is not null)
            {
                _hrefMaxProduct = $"/product/{_maxChange.Store}/{_maxChange.Name}-{_maxChange.Identifier}";
            }
            _showSpinner = false;
        }
    }
}