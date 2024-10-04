using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Configuration;

namespace CheckDiePreise.Components.Pages
{
    public partial class AdminSite
    {
        private Dictionary<string, int> todaysPriceChanges = [];
        private Dictionary<string, int> reciveDataUntilHour = new Dictionary<string, int>
        {
            { "ALDI SUED", 11 },
            { "Hellweg", 14 },
            { "IKEA", 15 },
            { "LEGO", 13 },
            { "ShopApotheke", 9 },
            { "LIDL", 12 },
        };
        private Dictionary<string, DailyReport> todaysDailyReports = [];
        private IEnumerable<DailyReport> DailyReports = new List<DailyReport>();
        private List<string> _availableStores = [];

        private string _adminPassword = "None";

        [Inject] IConfiguration Configuration { get; set; } = null!;

        [Inject]
        private PriceService PriceService { get; set; } = null!;

        protected override async Task OnInitializedAsync()
        {
            base.OnInitialized();
            _adminPassword = Environment.GetEnvironmentVariable("adminpassword");

            #if DEBUG
            _adminPassword = "debuggi";
            #endif
            _availableStores = Configuration.GetValue<string>("Stores").Split(",").ToList();

            foreach(var _availableStore in _availableStores)
            {
                var priceChangeCount = await PriceService.GetTodaysNewPriceChangesCountForStoreAsync(_availableStore);
                var todaysDailyReport = await PriceService.GetTodaysDailyReportByStore(_availableStore);

                todaysPriceChanges.Add(_availableStore, priceChangeCount);
                todaysDailyReports.Add(_availableStore, todaysDailyReport);
               
            }
        }
    }
}
