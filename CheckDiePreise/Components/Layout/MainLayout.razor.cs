using Microsoft.AspNetCore.Components;
using MudBlazor;

namespace CheckDiePreise.Components.Layout;

public partial class MainLayout
{

    bool _drawerOpen = true;

    [Inject] 
    private NavigationManager NavigationManager { get; set; } = null!;

    void DrawerToggle(string page = "")
    {
        _drawerOpen = !_drawerOpen;
        NavigationManager.NavigateTo($"/{page}");
    }

    MudTheme MyCustomTheme = new MudTheme()
    {
        PaletteLight = new PaletteLight()
        {
            Primary = MudBlazor.Colors.Amber.Default,
            Secondary = MudBlazor.Colors.Green.Accent4,
            Tertiary = MudBlazor.Colors.Gray.Lighten5,
            AppbarBackground = MudBlazor.Colors.Amber.Default,
        },

    };

}
