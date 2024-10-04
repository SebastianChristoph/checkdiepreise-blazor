using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;

namespace CheckDiePreise.Components.Pages
{
    public partial class AdminSite
    {
        private Dictionary<string, int> yesterdaysPriceChanges = [];
        //private Dictionary<string, int> reciveDataUntilHour = new Dictionary<string, int>
        //{
        //    { "ALDI SUED", 11 },
        //    { "Hellweg", 15 },
        //    { "IKEA", 16 },
        //    { "LEGO", 14 },
        //    { "ShopApotheke", 10 },
        //    { "LIDL", 13 },
        //};
        private Dictionary<string, DailyReport> yesterdaysDailyReports = [];
        private IEnumerable<DailyReport> DailyReports = new List<DailyReport>();
        private List<string> _availableStores = [];

        private string _adminPassword = "None";
        private string _userPasswordInput = string.Empty;

        [Inject] IConfiguration Configuration { get; set; } = null!;

        [Inject]
        private PriceService PriceService { get; set; } = null!;

        protected override async Task OnInitializedAsync()
        {
            base.OnInitialized();
            _adminPassword = Environment.GetEnvironmentVariable("adminpassword");

            #if DEBUG
            _adminPassword = "123";
            #endif

            _availableStores = Configuration.GetValue<string>("Stores").Split(",").ToList();

            foreach(var _availableStore in _availableStores)
            {
                var priceChangeCount = await PriceService.GetYesterdaysNewPriceChangesCountForStoreAsync(_availableStore);
                var yesterdaysDailyReport = await PriceService.GetYesterdaysDailyReportByStore(_availableStore);

                yesterdaysPriceChanges.Add(_availableStore, priceChangeCount);
                yesterdaysDailyReports.Add(_availableStore, yesterdaysDailyReport);
               
            }
        }
    }
}
