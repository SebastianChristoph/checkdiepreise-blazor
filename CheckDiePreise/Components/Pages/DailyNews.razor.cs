using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Configuration;
using static MudBlazor.CategoryTypes;

namespace CheckDiePreise.Components.Pages
{
    public partial class DailyNews
    {
        private bool _showSpinner = false;
        private List<string> _availableStores = [];
        private IEnumerable<ProductChange> ProductChanges = new List<ProductChange>();
        private string infoFormat = "{first_item}-{last_item} von {all_items}";
        [Inject] private PriceService PriceService { get; set; } = null!;
        [Inject] IConfiguration Configuration { get; set; } = null!;

        protected override async Task OnInitializedAsync()
        {
            base.OnInitialized();
            GetYesterdaysProductChangesByStore("all");
            _showSpinner = true;
            _availableStores = Configuration.GetValue<string>("Stores").Split(",").ToList();
            _availableStores.Sort();
        }

        private async Task GetYesterdaysProductChangesByStore(string storeName)
        {
            _showSpinner = true;
            StateHasChanged();
            await Task.Delay(1);
            ProductChanges = await PriceService.GetYesterdaysProductChanges(storeName);
            _showSpinner = false;
            StateHasChanged();
        }

    }
}