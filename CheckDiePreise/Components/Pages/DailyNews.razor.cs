using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Configuration;
using static MudBlazor.CategoryTypes;

namespace CheckDiePreise.Components.Pages
{
    public partial class DailyNews
    {
        private IEnumerable<ProductChange> ProductChanges = new List<ProductChange>();
        [Inject] private PriceService PriceService { get; set; } = null!;

        protected override async Task OnInitializedAsync()
        {
            base.OnInitialized();
            ProductChanges = await PriceService.GetTodaysProductChanges();
            if (!ProductChanges.Any())
            {
                ProductChanges = await PriceService.GetRandomProductsAsync();
            }
        }

    }
}