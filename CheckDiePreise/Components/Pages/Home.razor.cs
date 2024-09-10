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
        private DailyStats _dailyStats;
        private string _hrefMaxProduct = string.Empty;
        private string _hrefMinProduct = string.Empty;

        [Inject]
        private PriceService PriceService{ get; set; } = null!;

        [Inject] IConfiguration Configuration { get; set; } = null!;

        protected override async Task OnInitializedAsync()
        {
            base.OnInitialized();
            _connectionString = Configuration.GetConnectionString("DefaultConnection");
            _canConnect = PriceService.CanConnectToDatabase();
            _usedDb = Configuration.GetValue<string>("UseDb");
            _dailyStats = await PriceService.GetLastDailyStat();
            if(_dailyStats is not null)
            {
                _hrefMinProduct = $"/product/{_dailyStats.MinStore}/{_dailyStats.MinName}-{_dailyStats.MinIdentifier}";
                _hrefMaxProduct = $"/product/{_dailyStats.MaxStore}/{_dailyStats.MaxName}-{_dailyStats.MaxIdentifier}";
            }
        }

       

    }
}