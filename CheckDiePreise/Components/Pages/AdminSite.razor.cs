using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Configuration;

namespace CheckDiePreise.Components.Pages
{
    public partial class AdminSite
    {
        private Dictionary<string, int> todaysPriceChanges = [];
        private Dictionary<string, DailyReport> todaysDailyReports = [];
        private IEnumerable<DailyReport> DailyReports = new List<DailyReport>();
        private List<string> _availableStores = [];

        [Inject] IConfiguration Configuration { get; set; } = null!;

        [Inject]
        private PriceService PriceService { get; set; } = null!;

        protected override async Task OnInitializedAsync()
        {
            base.OnInitialized();
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
