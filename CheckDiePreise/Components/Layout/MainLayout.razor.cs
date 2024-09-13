using Microsoft.AspNetCore.Components;
using MudBlazor;

namespace CheckDiePreise.Components.Layout;

public partial class MainLayout
{

    bool _drawerOpen = true;
    private string _quicksearch ="Produkt-Schnellsuche";

    [Inject] 
    private NavigationManager NavigationManager { get; set; } = null!;

    void DrawerToggle(string page)
    {
        _drawerOpen = !_drawerOpen;
        NavigationManager.NavigateTo($"/{page}");
    }

    void DrawerToggle()
    {
        _drawerOpen = !_drawerOpen;
    }

    MudTheme MyCustomTheme = new MudTheme()
    {
        PaletteLight = new PaletteLight()
        {
            Primary = "#53B3DB",
            Secondary = "#DC9B53",
            Tertiary = "#867460",
            AppbarBackground = "#53B3DB",
        },

    };

}
