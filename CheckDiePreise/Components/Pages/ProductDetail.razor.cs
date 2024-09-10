using CheckDiePreise.Data.Models;
using CheckDiePreise.Data.Services;
using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Configuration;

namespace CheckDiePreise.Components.Pages
{
    public partial class ProductDetail
    {

        private List<ProductChange> _productChanges;
        [Parameter] public string? Store { get; set; }
        [Parameter] public string? Name { get; set; }
        [Parameter] public string? Identifier { get; set; }

        [Inject]
        private PriceService PriceService { get; set; } = null!;

        protected override async Task OnInitializedAsync()
        {
            base.OnInitialized();
            _productChanges = await PriceService.GetAllProductChangesOfProductAsync(Store, Identifier);
        }
    }
}
