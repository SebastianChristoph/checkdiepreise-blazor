using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;

namespace CheckDiePreise.Components.Pages
{
    public partial class StoreAnalysis
    {
        private List<StorePriceChange>? _storePriceChanges;
        
        [Inject] 
        private PriceService PriceService { get; set; } = null!;

        protected override async Task OnInitializedAsync()
        {
            base.OnInitialized();
            _storePriceChanges = await PriceService.GetStorePriceChangesByStore("LIDL");
        }
    }
}