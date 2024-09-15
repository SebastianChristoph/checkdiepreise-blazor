using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;

namespace CheckDiePreise.Components.Pages
{
    public partial class AdminSite
    {
        private IEnumerable<DailyReport> DailyReports = new List<DailyReport>();
        [Inject]
        private PriceService PriceService { get; set; } = null!;

        protected override async Task OnInitializedAsync()
        {
            base.OnInitialized();
            DailyReports = await PriceService.GetLastDailyReports();
        }
    }
}